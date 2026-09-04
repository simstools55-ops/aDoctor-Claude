import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_versions():
    assert (ROOT/'VERSION').read_text().strip()=='1.5.1'
    assert (ROOT/'SHARED_VERSION').read_text().strip()=='3.5.0'

def test_presentation_docs_present():
    for n in ['PRESENTATION_STANDARD_V1.md','HUMAN_OUTPUT_POLICY_V1.md','MACHINE_OUTPUT_POLICY_V1.md','HUMAN_USABILITY_GATE_V1.md']:
        assert (ROOT/'shared'/'presentation'/n).exists()

def test_case_result_schema_has_presentation():
    d=json.loads((ROOT/'contracts'/'SIMS_DOCTOR_CASE_RESULT_V2.schema.json').read_text())
    p=d['properties']['presentation']
    assert p['properties']['standard']['const']=='SIMS_PRESENTATION_STANDARD_V1'
    assert set(['summary','do_now','do_not','next_step']).issubset(p['properties'])

def test_a900024_example_human_layer():
    d=json.loads((ROOT/'Examples'/'a900024-algorithm-light-fix-presentation.example.json').read_text())
    assert d['treatment_plan']['strategy']=='LIGHT_FIX'
    assert d['presentation']['standard']=='SIMS_PRESENTATION_STANDARD_V1'
    assert d['presentation']['review_after_days']==28
    assert 'allowed_scope' not in d['presentation']
    assert d['workflow_handoff']['next_action']=='WRITER'

def test_instructions_define_boundary():
    t=(ROOT/'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text()
    assert 'Human Experience / Presentation Framework' in t
    assert 'DoctorはBefore/After修正文を生成しない' in t
