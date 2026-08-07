from qa import validate_manifest


def test_validate_manifest_accepts_completed_manifest():
    manifest = {
        "schema_version": 1,
        "generator": "productvideo",
        "topic": "Test",
        "status": "completed",
        "runtime": {},
        "models": {},
        "artifacts": {},
        "error": None,
    }
    assert validate_manifest(manifest).ok


def test_validate_manifest_rejects_unknown_status():
    manifest = {"schema_version": 1, "status": "unknown"}
    result = validate_manifest(manifest)
    assert not result.ok
    assert "Ungültiger Manifest-Status" in result.errors
