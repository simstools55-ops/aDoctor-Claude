from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_INTERNAL_PATH = 100


def _distribution_files():
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        parts = set(p.relative_to(ROOT).parts)
        if '.pytest_cache' in parts or '__pycache__' in parts or p.suffix == '.pyc':
            continue
        yield p

def test_distribution_has_no_python_cache_artifacts():
    bad = [p for p in ROOT.rglob('*') if p.is_file() and ('.pytest_cache' in p.parts or '__pycache__' in p.parts or p.suffix == '.pyc')]
    assert not bad

def test_distribution_internal_paths_are_windows_safe():
    paths = [p.relative_to(ROOT).as_posix() for p in _distribution_files()]
    longest = max(paths, key=len)
    assert len(longest) <= MAX_INTERNAL_PATH, f'{len(longest)}: {longest}'
