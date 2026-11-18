# Validation

Run the offline regression suites from this directory:

```sh
python -B scripts/run_validation.py --suite brain
python -B scripts/run_validation.py --suite cell
python -B -m unittest discover -s tests/memory
python -B -m unittest discover -s tests/downstream
python -B -m unittest discover -s colombo_memory_agent/tests
```

The suites use simulated model/API backends and local workers. Compiler tests
require an independently provisioned Lean environment. Keep test execution
output outside the source distribution.
