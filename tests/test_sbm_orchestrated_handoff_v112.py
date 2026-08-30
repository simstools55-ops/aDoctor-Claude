from pathlib import Path

def test_instructions_require_sbm_result_json():
    root=Path(__file__).resolve().parents[1]
    text=(root/"CLAUDE_PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert "SBM → Doctor → SBM → Writer / Creator / Merge → SBM" in text
    assert "SIMS_DOCTOR_CASE_RESULT_V2" in text
    assert "DoctorからWriter / Creator / Mergeへ直接渡すコピー用依頼文を表示しない" in text
    assert "REQUIRED_SBM_REGISTRATION" in text
