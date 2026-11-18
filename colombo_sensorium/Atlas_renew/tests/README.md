# Public regression tests

These self-contained tests use invented contracts and immutable in-memory baselines. They check stale patches, stable IDs, scientific contract preservation, comparison scope, evidence-only changes, independent source-reading requirements, and exact prepared-bundle binding. They call no external model or network service and write no existing Atlas.

After installing Atlas_renew and its source backend in a dedicated virtual environment, run `python -m pytest tests`. The historical full acceptance fixtures are intentionally excluded from this public directory. Passing these synthetic tests is not a scientific review or evidence of a real model run.
