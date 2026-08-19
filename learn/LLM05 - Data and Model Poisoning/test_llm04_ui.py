from pathlib import Path

APP_PATH = Path(__file__).parent / "app.py"


def test_llm04_levels_include_dedicated_upload_panel():
    text = APP_PATH.read_text(encoding="utf-8")
    assert "upload-panel" in text
    assert "Download baseline CSV" in text
    assert "Upload modified CSV" in text
    assert "Score uploaded CSV" in text
