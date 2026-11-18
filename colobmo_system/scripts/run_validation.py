"""Run offline regression suites with workspace-local temporary files and logs."""
import argparse
from contextlib import redirect_stdout, redirect_stderr
import os
from pathlib import Path
import sys
import tempfile
import unittest


CURRENT_TESTS = (
    "test_budget_policy.py",
    "test_claim_provenance.py",
    "test_controller_recovery.py",
    "test_empirical_observations.py",
    "test_experiment_dispatch.py",
    "test_final_publication.py",
    "test_integration_activity.py",
    "test_integration_structure.py",
    "test_layout.py",
    "test_mcp_transport.py",
    "test_oracle_workflow.py",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=("current", "brain", "cell"), default="current")
    parser.add_argument("--pattern", help="Run one matching offline test module/group")
    parser.add_argument("--output-dir", type=Path,
                        help="Keep logs and temporary files in a separate validation directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (args.output_dir or root / "validation" / "offline").resolve()
    temporary = output / "tmp"
    temporary.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(temporary)
    source = root / "tests" / ("cell" if args.suite == "cell" else "brain")
    os.chdir(root)
    sys.path[:0] = [str(root / "src"), str(source)]
    if args.pattern:
        suite = unittest.defaultTestLoader.discover(str(source), pattern=args.pattern)
    elif args.suite == "current":
        suite = unittest.TestSuite([
            unittest.defaultTestLoader.discover(str(source), pattern=pattern)
            for pattern in CURRENT_TESTS
        ])
    else:
        suite = unittest.defaultTestLoader.discover(str(source))
    label = args.pattern.replace("*", "all").replace(".py", "") if args.pattern else args.suite
    log = output / (label + "-tests.log")
    with log.open("w", encoding="utf-8") as stream:
        with redirect_stdout(stream), redirect_stderr(stream):
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print(f"{args.suite}: {result.testsRun} tests, {len(result.failures)} failures, "
          f"{len(result.errors)} errors, {len(result.skipped)} skipped")
    for test, details in [*result.failures, *result.errors]:
        print(test, details.splitlines()[-1])
    print(log)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
