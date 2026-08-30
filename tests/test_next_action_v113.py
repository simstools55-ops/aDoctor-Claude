from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_next_action_instruction():
 assert 'workflow_handoff.next_action' in (ROOT/'PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
