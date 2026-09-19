from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def check(base):
    policy=json.loads((base/'Knowledge/algorithm_impact/algorithm_impact_policy_v1.json').read_text(encoding='utf-8'))
    assert policy['principles']['algorithm_update_is_evidence_not_diagnosis'] is True
    assert policy['principles']['temporal_overlap_alone_is_insufficient'] is True
    schema=json.loads((base/'contracts/SIMS_DOCTOR_ALGORITHM_IMPACT_ASSESSMENT_V1.schema.json').read_text(encoding='utf-8'))
    assert schema['properties']['contract_name']['const']=='SIMS_DOCTOR_ALGORITHM_IMPACT_ASSESSMENT_V1'
    ins=(base/'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'Googleアップデートは診断結果ではなく' in ins
    assert '`WAIT` は放置ではない' in ins
    for name in ['algorithm-impact-wait.example.json','algorithm-impact-rewrite.example.json']:
        assert (base/'Examples'/name).exists()

def test_root_algorithm_package(): check(ROOT)
def test_upload_algorithm_package(): check(ROOT/'Claude-Upload')
