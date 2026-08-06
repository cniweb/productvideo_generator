import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from pytrends.request import TrendReq
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ==============================================================================
# KONFIGURATION & API KEYS
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")
with open(os.path.join(SCRIPT_DIR, "VERSION"), encoding="utf-8") as version_file:
    VERSION = version_file.read().strip()
load_dotenv(ENV_FILE)

def _raise_env_error(message, missing=None):
    details = ""
    if missing:
        missing_list = ", ".join(missing)
        details = f"\n   Fehlende Variablen: {missing_list}"
    raise RuntimeError(
        "❌ Konfiguration fehlt.\n"
        f"   {message}"
        f"{details}\n"
        "   Nächster Schritt: Kopiere .env.example nach .env und setze die Variablen."
    )


REQUIRED_ENV_VARS = [
    "GEMINI_API_KEY",
    "CHANNEL_NAME",
    "CHANNEL_DESCRIPTION",
    "VIDEO_OUTPUT_DIR",
    "VIDEO_MODEL",
    "VIDEO_FALLBACK_MODEL",
]

MIN_TOPIC_LENGTH = 3

def _check_env_file():
    """Check if .env file exists and contains required variables.
    Only called when the module is used, not at import time."""
    missing_env = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    # Allow either .env file OR environment variables to be set
    if not os.path.exists(ENV_FILE) and missing_env:
        _raise_env_error(
            "Keine .env Datei gefunden und nicht alle Umgebungsvariablen sind gesetzt.",
            missing=missing_env,
        )
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


def normalize_topic(topic, min_length=MIN_TOPIC_LENGTH, fallback="topic"):
    cleaned = "" if topic is None else str(topic).strip()
    if not cleaned:
        return fallback
    normalized = unicodedata.normalize("NFKD", cleaned)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    normalized = re.sub(r"[^\w]+", "_", normalized, flags=re.UNICODE)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    if len(normalized) < min_length:
        return fallback
    return normalized

# Global variables - initialized lazily
GEMINI_API_KEY = None
CHANNEL_NAME = None
CHANNEL_DESC = None
OUTPUT_DIR = None
client = None

# Modelle - constants can stay
SCRIPT_MODEL = "gemini-3-pro-preview"
VIDEO_MODEL = None
VIDEO_FALLBACK_MODEL = None
VIDEO_MAX_SECONDS = None
VIDEO_ASPECT_RATIO = None
VIDEO_RESOLUTION = None
VIDEO_GENERATION_WAIT_MESSAGE = "   ⏳ Warte auf Video-Generierung..."
VIDEO_NO_DATA_ERROR_MESSAGE = "API lieferte keine Video-Daten zurück."

_initialized = False

def _initialize_config():
    """Initialize configuration and API client. Called lazily on first use."""
    global GEMINI_API_KEY, CHANNEL_NAME, CHANNEL_DESC, OUTPUT_DIR, client
    global VIDEO_MODEL, VIDEO_FALLBACK_MODEL
    global VIDEO_MAX_SECONDS, VIDEO_ASPECT_RATIO, VIDEO_RESOLUTION, _initialized
    
    if _initialized:
        return
    
    _check_env_file()
    
    # Secrets
    GEMINI_API_KEY = _require_env("GEMINI_API_KEY")
    
    # Kanal Einstellungen
    CHANNEL_NAME = _require_env("CHANNEL_NAME")
    CHANNEL_DESC = _require_env("CHANNEL_DESCRIPTION")
    
    # Pfade
    OUTPUT_DIR = _require_env("VIDEO_OUTPUT_DIR")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Client-Setup (only if not already set, e.g., in tests)
    if client is None:
        client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Video configuration
    VIDEO_MODEL = _require_env("VIDEO_MODEL")
    VIDEO_FALLBACK_MODEL = _require_env("VIDEO_FALLBACK_MODEL")
    VIDEO_MAX_SECONDS = _optional_int_env("VIDEO_MAX_SECONDS", 10)
    VIDEO_ASPECT_RATIO = _optional_env("VIDEO_ASPECT_RATIO", "9:16")
    VIDEO_RESOLUTION = _optional_env("VIDEO_RESOLUTION", "720p")

    used_defaults = []
    if os.getenv("VIDEO_MAX_SECONDS") in (None, ""):
        used_defaults.append(f"VIDEO_MAX_SECONDS={VIDEO_MAX_SECONDS}")
    if os.getenv("VIDEO_ASPECT_RATIO") in (None, ""):
        used_defaults.append(f"VIDEO_ASPECT_RATIO={VIDEO_ASPECT_RATIO}")
    if os.getenv("VIDEO_RESOLUTION") in (None, ""):
        used_defaults.append(f"VIDEO_RESOLUTION={VIDEO_RESOLUTION}")
    if used_defaults:
        print(f"   ℹ️ Nutze Standardwerte: {', '.join(used_defaults)}")
    
    _initialized = True


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
        _initialize_config()  # Ensure configuration is loaded
        self.topic = topic
        self.script_content = ""
        self.video_path = ""
        self.script_path = ""
        self.metadata_path = ""
        self.run_manifest_path = ""
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
        print(f"✍️ 2. Erstelle Produkt-Skript für '{self.topic}'...")

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
            normalized_topic = normalize_topic(self.topic)
            script_filename = f"{normalized_topic}_script.txt"
            script_path = os.path.join(OUTPUT_DIR, script_filename)
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(self.script_content)
            self.script_path = script_path
            
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
        fallback_candidates = [
            VIDEO_FALLBACK_MODEL,
        ]

        candidates = _list_video_models()
        if candidates:
            print(f"   💡 Verfügbare Video-Modelle: {', '.join(candidates)}")
            for candidate in candidates:
                if candidate not in fallback_candidates:
                    fallback_candidates.append(candidate)

        fallback = None
        for candidate in fallback_candidates:
            if candidate and candidate != video_model:
                fallback = candidate
                break
        if fallback is None:
            print("   💡 Setze VIDEO_MODEL/VIDEO_FALLBACK_MODEL in .env auf verfügbare Modelle.")
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
        print("   💡 Setze VIDEO_MODEL/VIDEO_FALLBACK_MODEL in .env auf verfügbare Modelle.")
        return False

    def generate_video_with_veo(self):
        """Nutzt die Gemini API (Veo Modell), um das Video zu rendern."""
        video_model = VIDEO_MODEL
        print(f"🎬 3. Generiere Video mit {video_model} (das kann dauern)...")

        veo_prompt = self._build_veo_prompt()

        try:
            normalized_topic = normalize_topic(self.topic)
            filename = f"{normalized_topic}.mp4"
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

        normalized_topic = normalize_topic(self.topic)
        script_path = self.script_path or os.path.join(
            OUTPUT_DIR,
            f"{normalized_topic}_script.txt",
        )
        video_path = self.video_path or os.path.join(
            OUTPUT_DIR,
            f"{normalized_topic}.mp4",
        )
        meta = {
            "channel": CHANNEL_NAME,
            "topic": self.topic,
            "generator_version": VERSION,
            "runtime": {
                "python": platform.python_version(),
                "platform": platform.platform(),
            },
            "video_file": video_path,
            "script_file": script_path,
            "youtube_title": data.get("title", f"Review: {self.topic}"),
            "youtube_description": data.get("description", ""),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        meta_path = os.path.join(OUTPUT_DIR, f"{normalized_topic}_meta.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4, ensure_ascii=False)
        self.metadata_path = meta_path
        print("   -> Fertig.")

    def write_run_manifest(self, *, started_at, finished_at, status, error=None):
        """Schreibt den standardisierten Status des Produktionslaufs."""
        normalized_topic = normalize_topic(self.topic)
        manifest = {
            "topic": self.topic,
            "status": status,
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_seconds": round(max(0.0, finished_at - started_at), 2),
            "models": {
                "script": SCRIPT_MODEL,
                "video": VIDEO_MODEL,
                "video_fallback": VIDEO_FALLBACK_MODEL,
            },
            "artifacts": {
                "script": self.script_path or None,
                "video": self.video_path or None,
                "metadata": self.metadata_path or None,
            },
            "error": error,
        }
        self.run_manifest_path = os.path.join(
            OUTPUT_DIR, f"{normalized_topic}_run.json"
        )
        with open(self.run_manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    def validate_outputs(self):
        """Prüft alle erzeugten Productvideo-Artefakte vor dem Erfolgsstatus."""
        issues = []
        required_files = {
            "Skript-Datei": self.script_path,
            "Video-Datei": self.video_path,
            "Metadaten-Datei": self.metadata_path,
        }
        for label, path in required_files.items():
            if not path or not os.path.exists(path):
                issues.append(f"{label} fehlt")
            elif os.path.getsize(path) == 0:
                issues.append(f"{label} ist leer")

        if self.metadata_path and os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, encoding="utf-8") as f:
                    metadata = json.load(f)
                for key in ("video_file", "script_file"):
                    referenced = metadata.get(key)
                    if referenced and not os.path.exists(referenced):
                        issues.append(f"Metadaten-Referenz fehlt: {key}")
            except (OSError, json.JSONDecodeError) as exc:
                issues.append(f"Metadaten-JSON ungültig: {exc}")

        ffprobe = shutil.which("ffprobe")
        if ffprobe and self.video_path and os.path.exists(self.video_path):
            result = subprocess.run(
                [
                    ffprobe,
                    "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=codec_type",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    self.video_path,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0 or "video" not in result.stdout.split():
                issues.append("Video-Datei enthält keinen lesbaren Videostream")
        elif not ffprobe:
            print("   ⚠️ ffprobe nicht verfügbar – überspringe Video-Stream-Prüfung.")

        if issues:
            raise RuntimeError("Output-QA fehlgeschlagen: " + "; ".join(issues))


def _raise_input_error(reason):
    raise RuntimeError(
        "❌ Ungültiger Topic-Input.\n"
        f"   {reason}\n"
        f"   Nächster Schritt: Gib ein Produkt/Thema mit mindestens {MIN_TOPIC_LENGTH} Zeichen an "
        "(z. B. \"Smarte Kaffeemaschine\")."
    )


def _validate_topic_input(topic):
    if not topic or len(topic.strip()) < MIN_TOPIC_LENGTH:
        _raise_input_error(f"Topic muss mindestens {MIN_TOPIC_LENGTH} Zeichen haben.")


def _resolve_topic_from_cli(argv=None):
    parser = argparse.ArgumentParser(description="Product Video Generator (Veo)")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument(
        "topic",
        nargs="?",
        help=f"Produkt/Thema (min. {MIN_TOPIC_LENGTH} Zeichen)",
    )
    args = parser.parse_args(argv)

    if args.topic is not None:
        topic = args.topic.strip()
        _validate_topic_input(topic)
        return topic

    if not sys.stdin.isatty():
        stdin_topic = sys.stdin.read().strip()
        _validate_topic_input(stdin_topic)
        return stdin_topic

    prompt = (
        f"Produkt/Thema (min. {MIN_TOPIC_LENGTH} Zeichen, z. B. \"Smarte Kaffeemaschine\"): "
    )
    try:
        topic = input(prompt).strip()
    except EOFError:
        topic = ""
    _validate_topic_input(topic)
    return topic

# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == "__main__":
    _initialize_config()  # Initialize before using config variables
    print(f"--- {CHANNEL_NAME.upper()} GENERATOR (VEO) ---")
    run_started_at = time.time()

    # Eingabe lesen (CLI-Argument > stdin > Prompt)
    topic = _resolve_topic_from_cli()

    gen = ProductVideoGenerator(topic)

    try:
        gen.research_trends()
        gen.generate_sales_script()
        if not gen.script_content:
            raise RuntimeError("Kein Skript erzeugt.")
        gen.generate_video_with_veo()
        gen.generate_metadata()
        gen.validate_outputs()
    except Exception as exc:
        gen.write_run_manifest(
            started_at=run_started_at,
            finished_at=time.time(),
            status="failed",
            error=str(exc),
        )
        raise

    gen.write_run_manifest(
        started_at=run_started_at,
        finished_at=time.time(),
        status="completed",
    )
    print("\n✅ PRODUKTION ABGESCHLOSSEN!")
