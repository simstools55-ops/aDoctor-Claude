from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def text(rel): return (ROOT/rel).read_text(encoding="utf-8")

def test_gate_instructions_present():
    for rel in ["CLAUDE_PROJECT_INSTRUCTIONS.md","PROJECT_INSTRUCTIONS.md","Claude-Upload/CLAUDE_PROJECT_INSTRUCTIONS.md","Claude-Upload/PROJECT_INSTRUCTIONS.md"]:
        t=text(rel)
        assert "PROTOCOL=SIMS-A/1" in t
        assert "SOURCE=SIMS_MANAGER" in t
        assert "EDITION=FULL" in t
        assert "TARGET=ADOCTOR" in t
        assert "診断処理、Web/SERP調査、記事評価、JSON生成を開始してはならない" in t

def test_release_version():
    assert text("VERSION").strip()=="1.5.2"
    assert text("Claude-Upload/VERSION").strip()=="1.5.2"
