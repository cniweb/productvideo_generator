import importlib
import json
from types import SimpleNamespace


def _load_module(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("CHANNEL_NAME", "Test Channel")
    monkeypatch.setenv("CHANNEL_DESCRIPTION", "Test Desc")
    monkeypatch.setenv("VIDEO_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("VIDEO_MODEL", "test-video-model")
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


def test_generate_sales_script_writes_file(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.client = DummyClient(pv)

    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.generate_sales_script()

    assert "Skripttext" in gen.script_content
    script_path = tmp_path / "TestProdukt_script.txt"
    assert script_path.exists()
    assert script_path.read_text(encoding="utf-8") == gen.script_content


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
