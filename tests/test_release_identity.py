import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = '1.5.1'


def verify(base: Path):
    assert (base / 'VERSION').read_text(encoding='utf-8').strip() == EXPECTED
    identity = json.loads((base / 'PRODUCT_IDENTITY.json').read_text(encoding='utf-8'))
    assert identity['package_version'] == EXPECTED
    package = json.loads((base / 'CLAUDE_PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    assert package['package_version'] == EXPECTED
    deployment = json.loads((base / 'CLAUDE_DEPLOYMENT_MANIFEST.json').read_text(encoding='utf-8'))
    assert deployment['package_version'] == EXPECTED
    instructions = (base / 'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert instructions.splitlines()[0] == f'# aDoctor Claude v{EXPECTED} — Site Primary Doctor'
    assert f'v{EXPECTED}' in instructions


def test_repository_identity():
    verify(ROOT)


def test_claude_upload_identity():
    verify(ROOT / 'Claude-Upload')
