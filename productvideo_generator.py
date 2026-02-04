import os
import json
import time
from pytrends.request import TrendReq
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ==============================================================================
# KONFIGURATION & API KEYS
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")
load_dotenv(ENV_FILE)

def _raise_env_error(message, missing=None):
    details = ""
    if missing:
        missing_list = ", ".join(missing)
        details = f"\n   Fehlende Variablen: {missing_list}"
    raise RuntimeError(
        "❌ Konfiguration fehlt.\n"
        f"   {message}\n"
        "   Lege eine .env Datei im Projektverzeichnis an oder setze die Variablen als Umgebungsvariablen."
        f"\n   Beispiel .env:\n   GEMINI_API_KEY=...\n   CHANNEL_NAME=...\n   CHANNEL_DESCRIPTION=...\n   VIDEO_OUTPUT_DIR=..."
        f"{details}"
    )


REQUIRED_ENV_VARS = [
    "GEMINI_API_KEY",
    "CHANNEL_NAME",
    "CHANNEL_DESCRIPTION",
    "VIDEO_OUTPUT_DIR",
]

if not os.path.exists(ENV_FILE):
    _raise_env_error("Keine .env Datei gefunden.")

missing_env = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
if missing_env:
    _raise_env_error("Die .env Datei ist unvollständig oder leer.", missing=missing_env)

def _require_env(var_name):
    value = os.getenv(var_name)
    if not value:
        _raise_env_error(f"Umgebungsvariable '{var_name}' ist nicht gesetzt.", missing=[var_name])
    return value


def _optional_env(var_name, default=None):
    value = os.getenv(var_name)
    return value if value else default


def _optional_int_env(var_name, default):
    value = os.getenv(var_name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        print(f"   ⚠️ Ungültiger Wert für {var_name}, nutze Standard {default}.")
        return default

# Secrets
GEMINI_API_KEY = _require_env("GEMINI_API_KEY")

# Kanal Einstellungen
CHANNEL_NAME = _require_env("CHANNEL_NAME")
CHANNEL_DESC = _require_env("CHANNEL_DESCRIPTION")

# Pfade
OUTPUT_DIR = _require_env("VIDEO_OUTPUT_DIR")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Client-Setup
client = genai.Client(api_key=GEMINI_API_KEY)

# Modelle
SCRIPT_MODEL = "gemini-3-pro-preview"
VIDEO_MODEL = "veo-3.1-generate-preview"
VIDEO_MAX_SECONDS = _optional_int_env("VIDEO_MAX_SECONDS", 10)
VIDEO_ASPECT_RATIO = _optional_env("VIDEO_ASPECT_RATIO", "9:16")
VIDEO_RESOLUTION = _optional_env("VIDEO_RESOLUTION", "720p")
VIDEO_GENERATION_WAIT_MESSAGE = "   ⏳ Warte auf Video-Generierung..."
VIDEO_NO_DATA_ERROR_MESSAGE = "API lieferte keine Video-Daten zurück."


def _debug_print_models(models, limit=None):
    items = []
    for model in models:
        name = getattr(model, "name", None) or getattr(model, "id", None)
        if not name:
            continue
        methods = getattr(model, "supported_generation_methods", []) or []
        items.append((name, methods))

    if not items:
        print("   🐞 Verfügbare Modelle: keine")
        return

    total = len(items)
    preview = items if limit is None else items[:limit]
    print(f"   🐞 Verfügbare Modelle ({total}, Anzeige {len(preview)}):")
    for name, methods in preview:
        methods_text = ", ".join(methods) if methods else "-"
        print(f"      - {name} (methods: {methods_text})")
    if limit is not None and total > limit:
        print(f"      ... und {total - limit} weitere")


def _list_video_models():
    """Listet verfügbare Video-Modelle (best effort)."""
    try:
        models = list(client.models.list())
    except Exception as exc:
        print(f"   ⚠️ Model-Listing fehlgeschlagen: {exc}")
        return []

    video_models = []
    for model in models:
        name = getattr(model, "name", None) or getattr(model, "id", None)
        if not name:
            continue
        methods = getattr(model, "supported_generation_methods", []) or []
        if "generateContent" in methods or "generate_content" in methods:
            if "veo" in name.lower() or "video" in name.lower():
                video_models.append(name)
    print(f"   🐞 Gefundene Video-Modelle: {', '.join(video_models) if video_models else 'keine'}")
    if not video_models:
        _debug_print_models(models)
    return video_models

class ProductVideoGenerator:
    def __init__(self, topic):
        self.topic = topic
        self.script_content = ""
        self.video_path = ""
        print(f"🚀 Starte Videoproduktion für Kanal '{CHANNEL_NAME}'")
        print(f"   Thema: '{topic}'")

    def _build_video_config(self):
        """Erstellt die Konfiguration für Video-Ausgaben."""
        response_modalities = []
        if hasattr(types, "Modality"):
            video_modality = getattr(types.Modality, "VIDEO", None)
            if video_modality is None:
                video_modality = getattr(types.Modality, "MODALITY_VIDEO", None)
            if video_modality is not None:
                response_modalities = [video_modality]
            else:
                print("   ⚠️ SDK unterstützt Modality.VIDEO nicht – versuche ohne response_modalities.")
        else:
            print("   ⚠️ SDK unterstützt Modality nicht – versuche ohne response_modalities.")

        if response_modalities:
            return types.GenerateContentConfig(
                response_modalities=response_modalities,
                temperature=1.0
            )
        return types.GenerateContentConfig(
            temperature=1.0
        )

    def _extract_video_data(self, response):
        """Extrahiert Video-Daten aus der API-Antwort."""
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    return part.inline_data.data
        return None

    # --------------------------------------------------------------------------
    # 1. TRENDS (Google Trends)
    # --------------------------------------------------------------------------
    def research_trends(self):
        """Holt naheliegende Trends für das Thema aus Google Trends (DE)."""
        print("🔍 1. Analysiere Google Trends...")
        try:
            pytrends = TrendReq(hl='de', tz=120)
            # Suche nach Trends in Deutschland
            pytrends.build_payload([self.topic], cat=0, timeframe='today 1-m', geo='DE')
            related = pytrends.related_queries()
            
            if self.topic in related and related[self.topic]['top'] is not None:
                df = related[self.topic]['top']
                if not df.empty:
                    top_query = df.iloc[0]['query']
                    print(f"   -> Trend gefunden: '{top_query}'")
                    self.topic = top_query
            else:
                print("   -> Keine spezifischen Trends, nutze Ursprungsthema.")
        except Exception as e:
            # Bei API-Limits (429) oder Fehlern einfach weitermachen
            print(f"   ⚠️ Trend-Fehler (nutze Fallback): {e}")
        return self.topic

    # --------------------------------------------------------------------------
    # 2. VERKAUFS-SKRIPT (Gemini Text)
    # --------------------------------------------------------------------------
    def generate_sales_script(self):
        """Erstellt ein verkaufsoptimiertes Skript."""
        print(f"✍️  2. Erstelle Produkt-Skript für '{self.topic}'...")

        prompt = f"""
        Du bist der Produzent des Videokanals '{CHANNEL_NAME}'. Beschreibung: '{CHANNEL_DESC}'.
        Erstelle ein kurzes, verkaufsförderndes Video-Skript (max 60 Sekunden Sprechzeit) für das Produkt/Thema: '{self.topic}'.
        
        Struktur:
        1. **Hook**: Ein fesselnder erster Satz, der ein Problem anspricht oder Aufmerksamkeit erregt.
        2. **Solution**: Wie das Produkt/Thema das Problem löst.
        3. **Benefits**: 3 klare Vorteile (kurz und prägnant).
        4. **Call to Action (CTA)**: Klare Aufforderung das Produkt zu kaufen oder zu testen.

        Vorgaben:
        - Sprache: Deutsch.
        - Stil: Energetisch, überzeugend, professionell.
        - Formatierung: Reine Textausgabe des gesprochenen Wortes.
        - Wichtig: Füge in Klammern () kurze visuelle Hinweise für den Video-Generator hinzu (z.B. "Nahaufnahme Produkt", "Glückliche Person nutzt es"), aber halte den Haupttext fließend sprechbar.
        """
        
        try:
            response = client.models.generate_content(model=SCRIPT_MODEL, contents=prompt)
            self.script_content = response.text
            
            # Speichere Skript zur Kontrolle
            script_filename = f"{self.topic.replace(' ', '_')}_script.txt"
            script_path = os.path.join(OUTPUT_DIR, script_filename)
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(self.script_content)
            
            print("   -> Skript erstellt.")
        except Exception as e:
            raise RuntimeError(f"Skript Generierung fehlgeschlagen: {e}")

    # --------------------------------------------------------------------------
    # 3. VIDEO GENERIERUNG (Veo 3.1)
    # --------------------------------------------------------------------------
    def _build_veo_prompt(self):
        """Erstellt den Prompt für die Veo-Generierung."""
        return f"""
        Erstelle ein professionelles Produktvideo (Format 16:9, fotorealistisch) basierend auf diesem Skript.
        Das Video soll Hintergrundmusik und einen deutschen Sprecher enthalten, der den Text liest.
        
        Produkt: {self.topic}
        Stil: Hochwertige Werbeaufnahme, cinematisches Licht.
        
        Inhalt/Skript:
        {self.script_content}
        """

    def _wait_for_operation(self, operation, wait_message=VIDEO_GENERATION_WAIT_MESSAGE):
        """Wartet auf eine abgeschlossene Operation und gibt sie zurück."""
        while not operation.done:
            print(wait_message)
            time.sleep(10)
            operation = client.operations.get(operation)
        return operation

    def _run_video_generation(self, model, prompt, config=None, video=None):
        """Startet eine Video-Generierung und gibt das generierte Video zurück."""
        operation = client.models.generate_videos(
            model=model,
            prompt=prompt,
            video=video,
            config=config,
        )
        operation = self._wait_for_operation(operation)
        if not operation.response or not operation.response.generated_videos:
            raise RuntimeError(VIDEO_NO_DATA_ERROR_MESSAGE)
        return operation.response.generated_videos[0]

    def _extend_video_if_needed(self, video_model, veo_prompt, generated_video):
        """Verlängert das Video optional, falls möglich."""
        total_seconds = 8
        max_seconds = max(8, VIDEO_MAX_SECONDS)
        if VIDEO_ASPECT_RATIO != "16:9" and max_seconds > 8:
            return generated_video

        while VIDEO_ASPECT_RATIO == "16:9" and total_seconds < max_seconds:
            print(f"   ⏳ Verlängere Video ({total_seconds}s -> bis {max_seconds}s)...")
            generated_video = self._run_video_generation(
                model=video_model,
                prompt=veo_prompt,
                video=generated_video.video,
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    resolution="720p",
                ),
            )
            total_seconds += 7
        return generated_video

    def _save_generated_video(self, generated_video):
        """Speichert das generierte Video auf der Festplatte."""
        client.files.download(file=generated_video.video)
        generated_video.video.save(self.video_path)
        print(f"   -> Video gespeichert: {self.video_path}")

    def _retry_with_fallback_model(self, video_model, veo_prompt):
        """Versucht die Generierung mit einem Fallback-Modell."""
        candidates = _list_video_models()
        if not candidates:
            return False
        print(f"   💡 Verfügbare Video-Modelle: {', '.join(candidates)}")
        fallback = candidates[0]
        if fallback == video_model:
            print("   💡 Setze VIDEO_MODEL in .env auf eines der Modelle.")
            return False

        print(f"   🔁 Erneuter Versuch mit: {fallback}")
        try:
            generated_video = self._run_video_generation(
                model=fallback,
                prompt=veo_prompt,
            )
            self._save_generated_video(generated_video)
            return True
        except Exception as retry_exc:
            print(f"   ❌ Erneuter Versuch fehlgeschlagen: {retry_exc}")
        print("   💡 Setze VIDEO_MODEL in .env auf eines der Modelle.")
        return False

    def generate_video_with_veo(self):
        """Nutzt die Gemini API (Veo Modell), um das Video zu rendern."""
        video_model = VIDEO_MODEL
        print(f"🎬 3. Generiere Video mit {video_model} (das kann dauern)...")

        veo_prompt = self._build_veo_prompt()

        try:
            filename = f"{self.topic.replace(' ', '_')}.mp4"
            self.video_path = os.path.join(OUTPUT_DIR, filename)

            generated_video = self._run_video_generation(
                model=video_model,
                prompt=veo_prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio=VIDEO_ASPECT_RATIO,
                    resolution=VIDEO_RESOLUTION,
                    duration_seconds="8",
                ),
            )

            generated_video = self._extend_video_if_needed(
                video_model=video_model,
                veo_prompt=veo_prompt,
                generated_video=generated_video,
            )

            self._save_generated_video(generated_video)

        except Exception as e:
            print(f"   ❌ Veo Generierung Fehler: {e}")
            if "NOT_FOUND" in str(e):
                if self._retry_with_fallback_model(video_model, veo_prompt):
                    return

    # --------------------------------------------------------------------------
    # 4. METADATEN
    # --------------------------------------------------------------------------
    def generate_metadata(self):
        """Erstellt Titel und Beschreibung für Social Media."""
        print("📄 4. Generiere Metadaten...")
        
        prompt = (
            f"Erstelle einen knackigen YouTube-Titel und eine SEO-Beschreibung für: {self.topic}. "
            f"Basierend auf: {self.script_content}. "
            "JSON Format: {\"title\": \"...\", \"description\": \"...\"}"
        )
        
        try:
            resp = client.models.generate_content(model=SCRIPT_MODEL, contents=prompt)
            # Einfaches Parsing
            text = resp.text.strip()
            # Falls Markdown Code-Blöcke enthalten sind
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
        except Exception:
            data = {"title": self.topic, "description": self.script_content[:200]}

        meta = {
            "channel": CHANNEL_NAME,
            "topic": self.topic,
            "video_file": self.video_path,
            "script_file": os.path.join(OUTPUT_DIR, f"{self.topic.replace(' ', '_')}_script.txt"),
            "youtube_title": data.get("title", f"Review: {self.topic}"),
            "youtube_description": data.get("description", ""),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        meta_path = os.path.join(OUTPUT_DIR, f"{self.topic.replace(' ', '_')}_meta.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4, ensure_ascii=False)
        print("   -> Fertig.")

# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == "__main__":
    print(f"--- {CHANNEL_NAME.upper()} GENERATOR (VEO) ---")
    
    # Eingabe lesen (funktioniert auch via Pipe aus run.sh)
    try:
        topic = input("Produkt/Thema (Leer lassen für Trend): ").strip()
    except EOFError:
        topic = ""

    gen = ProductVideoGenerator(topic)

    gen.research_trends()
    
    gen.generate_sales_script()
    if gen.script_content:
        gen.generate_video_with_veo()
        gen.generate_metadata()
    
    print("\n✅ PRODUKTION ABGESCHLOSSEN!")
