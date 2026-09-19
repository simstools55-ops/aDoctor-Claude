# aDoctor Claude v1.5.2 Release Notes

- Added `SIMS Request Protocol Gate v1` before all diagnostic execution.
- Normal diagnosis now requires a Manager envelope with `SIMS-A/1`, `SIMS_MANAGER`, `FULL`, `ADOCTOR`, required IDs, and consistent Evidence IDs.
- Invalid/direct free-form requests return a fixed warning and do not start diagnosis, Web/SERP research, or result JSON generation.
- Explicitly documents that the gate is operational prompt control, not cryptographic authentication or a License Center replacement.
- Diagnosis logic, Shared Editorial Knowledge 3.5.0, and existing Doctor result contracts are unchanged.
