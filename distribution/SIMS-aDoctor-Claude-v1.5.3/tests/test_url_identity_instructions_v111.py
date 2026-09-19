from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_url_identity_rule_present_in_root_and_upload():
    for rel in ["CLAUDE_PROJECT_INSTRUCTIONS.md", "Claude-Upload/CLAUDE_PROJECT_INSTRUCTIONS.md"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "URL正規化・インデックス診断（v1.1.1）" in text
        assert "末尾スラッシュ" in text
        assert "Googleが選択した正規URL" in text
