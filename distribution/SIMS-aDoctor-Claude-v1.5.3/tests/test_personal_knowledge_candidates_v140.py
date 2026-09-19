import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_schema_has_optional_knowledge_candidates():
    d=json.loads((ROOT/'contracts'/'SIMS_DOCTOR_CASE_RESULT_V2.schema.json').read_text())
    assert 'knowledge_candidates' in d['properties']
    assert 'personal_knowledge_site_id' in d['properties']

def test_project_instructions_define_learning_boundary():
    t=(ROOT/'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text()
    assert 'Personal Knowledge 学習候補（v1.4.0）' in t
    assert 'confirmation_event_id' in t
    assert '現在順位' in t
