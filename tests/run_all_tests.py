"""
FRI Project Test Runner

Run from the project root:

    python tests/run_all_tests.py
"""

import sys
import unittest
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(project_root / "tests"),
        pattern="test_*.py",
        top_level_dir=str(project_root),
    )

    print("=" * 60)
    print("FINCRIME REGULATORY INTELLIGENCE")
    print("ENGINEERING TEST RUNNER")
    print("=" * 60)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Tests Run : {result.testsRun}")
    print(f"Failures  : {len(result.failures)}")
    print(f"Errors    : {len(result.errors)}")
    print(f"Status    : {'PASS' if result.wasSuccessful() else 'FAIL'}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())