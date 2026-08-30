from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_rc4_version_and_contract():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='1.4.4'
    assert (ROOT/'contracts/SIMS_DOCTOR_INTERNAL_LINK_RECOMMENDATION_V1.schema.json').exists()

def test_rc4_example_structured_recommendations():
    obj=json.loads((ROOT/'Examples/a900024-algorithm-light-fix-presentation.example.json').read_text(encoding='utf-8'))
    recs=obj['treatment_plan']['internal_link_recommendations']
    assert len(recs)==2
    assert all(r['writer_must_finalize_anchor'] is True for r in recs)
    assert obj['workflow_handoff']['internal_link_recommendations']==recs
