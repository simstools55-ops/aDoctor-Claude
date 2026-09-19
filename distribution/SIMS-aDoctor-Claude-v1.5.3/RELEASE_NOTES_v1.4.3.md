# SIMS Article Doctor Claude v1.4.3

## Windows ZIP path hotfix
- Fixes Windows Explorer error `0x80010135: パスが長すぎます`.
- The distribution ZIP no longer contains an extra product-name top directory; users may extract the ZIP into the folder Windows creates from the ZIP filename without duplicating the long product path.
- Removes `.pytest_cache`, `__pycache__`, and `.pyc` build/test artifacts from the distributed package.
- Adds a release regression test that caps the longest internal distribution path at 100 characters.
- No diagnosis logic, JSON contract, Personal Knowledge behavior, or target-site context-boundary behavior changed.
