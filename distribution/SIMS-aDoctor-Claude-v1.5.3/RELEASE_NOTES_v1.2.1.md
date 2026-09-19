# SIMS Article Doctor Claude v1.2.1

## Windows extraction hotfix
- Removed case-only duplicate `Contracts/` directories.
- Canonical contract directory is `contracts/`.
- Fixes Windows ZIP extraction overwrite prompts caused by `contracts/...` and `Contracts/...` resolving to the same path.
- Updated package tests to use the canonical lowercase directory.
- No diagnosis logic or JSON contract content changed.
