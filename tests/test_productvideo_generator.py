import importlib
import io
import json
import sys


def _load_module(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("CHANNEL_NAME", "Test Channel")
    monkeypatch.setenv("CHANNEL_DESCRIPTION", "Test Desc")
    monkeypatch.setenv("VIDEO_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("VIDEO_MODEL", "test-video-model")
    monkeypatch.setenv("VIDEO_FALLBACK_MODEL", "test-fallback-model")
    monkeypatch.setenv("VIDEO_MAX_SECONDS", "8")

    import productvideo_generator as pv

    pv = importlib.reload(pv)
    return pv


class DummyResponse:
    def __init__(self, text=None):
        self.text = text


class DummyVideoFile:
    def __init__(self, data):
        self._data = data

    def save(self, path):
        with open(path, "wb") as f:
            f.write(self._data)


class DummyGeneratedVideo:
    def __init__(self, data):
        self.video = DummyVideoFile(data)


class DummyOperationResponse:
    def __init__(self, data):
        self.generated_videos = [DummyGeneratedVideo(data)]


class DummyOperation:
    def __init__(self, data, done=True):
        self.done = done
        self.response = DummyOperationResponse(data) if done else None


class DummyModels:
    def __init__(self, pv):
        self.pv = pv

    def generate_content(self, model, contents, config=None):
        if model == self.pv.SCRIPT_MODEL and "JSON Format" in contents:
            payload = {"title": "Test Title", "description": "Test Desc"}
            return DummyResponse(text=json.dumps(payload))
        if model == self.pv.SCRIPT_MODEL:
            return DummyResponse(text="Skripttext (Nahaufnahme Produkt)")

    def generate_videos(self, model, prompt=None, video=None, config=None):
        return DummyOperation(b"FAKE_VIDEO_BYTES")


class DummyOperations:
    def get(self, operation):
        return operation


class DummyFiles:
    def download(self, file):
        return None


class DummyClient:
    def __init__(self, pv):
        self.models = DummyModels(pv)
        self.operations = DummyOperations()
        self.files = DummyFiles()


class DummyTrendReq:
    def __init__(self, *args, **kwargs):
        # Absichtlich leer: Dummy-Stub für Tests, keine Initialisierung nötig.
        pass

    def build_payload(self, *args, **kwargs):
        return None

    def related_queries(self):
        return {"TestProdukt": {"top": None}}


class DummyStdin(io.StringIO):
    def isatty(self):
        return False


def test_generate_sales_script_writes_file(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.client = DummyClient(pv)

    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.generate_sales_script()

    assert "Skripttext" in gen.script_content
    script_path = tmp_path / "TestProdukt_script.txt"
    assert script_path.exists()
    assert script_path.read_text(encoding="utf-8") == gen.script_content


def test_generate_content_retries_rate_limit(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    calls = {"count": 0}

    class RetryModels:
        def generate_content(self, **kwargs):
            calls["count"] += 1
            if calls["count"] == 1:
                raise RuntimeError("429 rate limit")
            return DummyResponse(text="ok")

    class RetryClient:
        models = RetryModels()

    pv.client = RetryClient()
    monkeypatch.setattr(pv.time, "sleep", lambda _: None)
    response = pv._generate_content_with_retry(model="test", contents="prompt")
    assert response.text == "ok"
    assert calls["count"] == 2


def test_generate_video_with_veo_writes_video(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.client = DummyClient(pv)

    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.script_content = "Skripttext"
    gen.generate_video_with_veo()

    assert gen.video_path
    video_path = tmp_path / "TestProdukt.mp4"
    assert video_path.exists()
    assert video_path.read_bytes() == b"FAKE_VIDEO_BYTES"


def test_wait_for_operation_times_out(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.VIDEO_POLL_MAX_ATTEMPTS = 2
    pv.VIDEO_POLL_INTERVAL_SECONDS = 0
    pv.client = DummyClient(pv)
    operation = DummyOperation(b"data", done=False)
    gen = pv.ProductVideoGenerator("TestProdukt")
    monkeypatch.setattr(pv.time, "sleep", lambda _: None)

    try:
        gen._wait_for_operation(operation)
    except pv.GenerationError as exc:
        assert "Zeitlimit" in str(exc)
    else:
        raise AssertionError("Polling sollte nach Maximalversuchen abbrechen")


def test_fallback_failure_raises_generation_error(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.VIDEO_FALLBACK_MODEL = "fallback"
    gen = pv.ProductVideoGenerator("TestProdukt")

    monkeypatch.setattr(
        gen,
        "_run_video_generation",
        lambda **_: (_ for _ in ()).throw(RuntimeError("video failed")),
    )
    monkeypatch.setattr(pv, "_list_video_models", lambda: [])

    try:
        gen._retry_with_fallback_model("primary", "prompt")
    except pv.GenerationError as exc:
        assert "Primäres" in str(exc)
    else:
        raise AssertionError("Fallbackfehler sollte GenerationError auslösen")


def test_atomic_json_write_replaces_target(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    target = tmp_path / "manifest.json"
    pv._atomic_write_json(str(target), {"status": "completed"})
    assert json.loads(target.read_text(encoding="utf-8"))["status"] == "completed"
    assert list(tmp_path.glob(".tmp-*")) == []


def test_generate_metadata_writes_json(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.client = DummyClient(pv)

    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.script_content = "Skripttext"
    gen.video_path = str(tmp_path / "TestProdukt.mp4")
    gen.generate_metadata()

    meta_path = tmp_path / "TestProdukt_meta.json"
    assert meta_path.exists()

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["youtube_title"] == "Test Title"
    assert meta["youtube_description"] == "Test Desc"


def test_research_trends_fallback(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    monkeypatch.setattr(pv, "TrendReq", DummyTrendReq)

    gen = pv.ProductVideoGenerator("TestProdukt")
    topic = gen.research_trends()

    assert topic == "TestProdukt"


def test_normalize_topic_handles_special_chars(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    normalized = pv.normalize_topic("  Smarte/ Kaffee   Maschine!  ")
    assert normalized == "Smarte_Kaffee_Maschine"


def test_generator_accepts_explicit_config(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    config = pv.load_config(
        {
            "GEMINI_API_KEY": "key",
            "CHANNEL_NAME": "Injected Channel",
            "CHANNEL_DESCRIPTION": "Injected Description",
            "VIDEO_OUTPUT_DIR": "injected-output",
            "VIDEO_MODEL": "injected-model",
            "VIDEO_FALLBACK_MODEL": "injected-fallback",
        },
        tmp_path,
    )
    generator = pv.ProductVideoGenerator("TestProdukt", config=config)
    assert generator.config is config


def test_normalize_topic_falls_back_for_short_input(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    normalized = pv.normalize_topic("x")
    assert normalized == "topic"


def test_check_env_file_missing_vars_message(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    monkeypatch.setenv("CHANNEL_NAME", "")
    monkeypatch.setattr(pv.os.path, "exists", lambda _: True)

    try:
        pv._check_env_file()
    except RuntimeError as exc:
        message = str(exc)
    else:
        raise AssertionError("_check_env_file sollte fehlende ENV-Keys melden")

    assert "Fehlende Variablen: CHANNEL_NAME" in message
    assert "Nächster Schritt: Kopiere .env.example nach .env" in message


def test_resolve_topic_prefers_cli_argument_over_stdin(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    monkeypatch.setattr(sys, "stdin", DummyStdin("PipeTopic"))
    topic = pv._resolve_topic_from_cli(["ArgTopic"])

    assert topic == "ArgTopic"


def test_cli_version_is_defined(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    assert pv.VERSION == "0.1.0"


def test_resolve_topic_reads_stdin_when_no_arg(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    monkeypatch.setattr(sys, "stdin", DummyStdin("PipeTopic"))
    topic = pv._resolve_topic_from_cli([])

    assert topic == "PipeTopic"


def test_resolve_topic_rejects_short_stdin(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    monkeypatch.setattr(sys, "stdin", DummyStdin("x"))
    try:
        pv._resolve_topic_from_cli([])
    except RuntimeError as exc:
        message = str(exc)
    else:
        raise AssertionError("Zu kurzer stdin-Input sollte fehlschlagen")

    assert "Ungültiger Topic-Input" in message


def test_initialize_config_creates_output_dir(tmp_path, monkeypatch):
    output_dir = tmp_path / "outputs" / "nested"
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("CHANNEL_NAME", "Test Channel")
    monkeypatch.setenv("CHANNEL_DESCRIPTION", "Test Desc")
    monkeypatch.setenv("VIDEO_OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("VIDEO_MODEL", "test-video-model")
    monkeypatch.setenv("VIDEO_FALLBACK_MODEL", "test-fallback-model")
    monkeypatch.setenv("VIDEO_MAX_SECONDS", "8")

    import productvideo_generator as pv

    pv = importlib.reload(pv)
    pv._initialize_config()

    assert output_dir.exists()


def test_optional_int_env_returns_default_for_invalid_value(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    monkeypatch.setenv("VIDEO_MAX_SECONDS", "not_a_number")
    result = pv._optional_int_env("VIDEO_MAX_SECONDS", 10)

    assert result == 10


def test_normalize_topic_handles_none_input(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    assert pv.normalize_topic(None) == "topic"


def test_normalize_topic_handles_umlauts(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    normalized = pv.normalize_topic("Smarte Kühlschränke für Büros")
    assert normalized == "Smarte_Kuhlschranke_fur_Buros"


def test_generate_metadata_fallback_on_invalid_json(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)

    class BrokenJsonClient:
        def __init__(self, pv_mod):
            self.models = BrokenJsonModels(pv_mod)
            self.operations = DummyOperations()
            self.files = DummyFiles()

    class BrokenJsonModels:
        def __init__(self, pv_mod):
            self.pv = pv_mod

        def generate_content(self, model, contents, config=None):
            return DummyResponse(text="this is not valid json")

    pv.client = BrokenJsonClient(pv)
    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.script_content = "Skripttext"
    gen.video_path = str(tmp_path / "TestProdukt.mp4")
    gen.generate_metadata()

    meta_path = tmp_path / "TestProdukt_meta.json"
    assert meta_path.exists()

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["youtube_title"] == "TestProdukt"
    assert meta["youtube_description"] == "Skripttext"


def test_initialize_config_skips_when_already_initialized(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.client = DummyClient(pv)

    pv._initialize_config()
    original_output_dir = pv.OUTPUT_DIR

    monkeypatch.setenv("VIDEO_OUTPUT_DIR", str(tmp_path / "other"))
    pv._initialize_config()

    assert pv.OUTPUT_DIR == original_output_dir


def test_write_run_manifest_persists_common_fields(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.script_path = str(tmp_path / "TestProdukt_script.txt")
    gen.video_path = str(tmp_path / "TestProdukt.mp4")
    gen.metadata_path = str(tmp_path / "TestProdukt_meta.json")

    gen.write_run_manifest(
        started_at=100.0,
        finished_at=112.5,
        status="completed",
    )

    manifest = json.loads(
        (tmp_path / "TestProdukt_run.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "completed"
    assert manifest["schema_version"] == 1
    assert manifest["generator"] == "productvideo"
    assert manifest["duration_seconds"] == 12.5
    assert manifest["artifacts"]["video"] == gen.video_path
    assert manifest["error"] is None


def test_manifest_serializes_structured_error(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    gen = pv.ProductVideoGenerator("TestProdukt")
    error = pv.GenerationError("temporary failure")
    gen.write_run_manifest(started_at=1.0, finished_at=2.0, status="failed", error=error)
    manifest = json.loads((tmp_path / "TestProdukt_run.json").read_text(encoding="utf-8"))
    assert manifest["error"]["type"] == "GenerationError"
    assert manifest["error"]["retryable"] is True


def test_validate_outputs_rejects_missing_artifacts(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    monkeypatch.setattr(pv.shutil, "which", lambda _: None)
    gen = pv.ProductVideoGenerator("TestProdukt")

    try:
        gen.validate_outputs()
    except RuntimeError as exc:
        assert "Output-QA fehlgeschlagen" in str(exc)
        assert "Skript-Datei fehlt" in str(exc)
        assert "Video-Datei fehlt" in str(exc)
    else:
        raise AssertionError("validate_outputs sollte fehlende Artefakte melden")


def test_validate_outputs_accepts_artifacts_without_ffprobe(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    monkeypatch.setattr(pv.shutil, "which", lambda _: None)
    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.script_path = str(tmp_path / "TestProdukt_script.txt")
    gen.video_path = str(tmp_path / "TestProdukt.mp4")
    gen.metadata_path = str(tmp_path / "TestProdukt_meta.json")
    for path in (gen.script_path, gen.video_path):
        open(path, "wb").write(b"artifact")
    with open(gen.metadata_path, "w", encoding="utf-8") as handle:
        json.dump(
            {"video_file": gen.video_path, "script_file": gen.script_path},
            handle,
        )

    gen.validate_outputs()


def test_validate_outputs_rejects_invalid_metadata_json(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    monkeypatch.setattr(pv.shutil, "which", lambda _: None)
    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.script_path = str(tmp_path / "script.txt")
    gen.video_path = str(tmp_path / "video.mp4")
    gen.metadata_path = str(tmp_path / "meta.json")
    for path in (gen.script_path, gen.video_path):
        open(path, "wb").write(b"artifact")
    open(gen.metadata_path, "w", encoding="utf-8").write("not json")

    try:
        gen.validate_outputs()
    except RuntimeError as exc:
        assert "Metadaten-JSON ungültig" in str(exc)
    else:
        raise AssertionError("Ungültiges JSON sollte die Output-QA stoppen")
