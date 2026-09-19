from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def text(): return (ROOT / "PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")

def test_gate_uses_existing_v2_contract():
    t=text()
    for token in ["SIMS_DOCTOR_SINGLE_CASE_REQUEST_V2","contract_version", "2.0", "schema_version", "2.0.0", "SIMS_BLOG_MANAGER", "SIMS_DOCTOR", "request.request_id", "site.site_id", "article.article_id"]:
        assert token in t

def test_obsolete_envelope_not_required():
    t=text()
    assert "追加の `[SIMS_REQUEST]` エンベロープは要求しない" in t

def test_rejection_message_present():
    assert "正規のaDoctor診断依頼として確認できません" in text()
