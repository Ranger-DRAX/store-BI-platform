"""
Superstore BI Automated Test Runner.
Executes test suites and prints structured test results.
"""

import unittest
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_data_loader import TestDataLoader
from tests.test_metrics import TestMetrics
from tests.test_scenario import TestScenario


def run_all_tests():
    print("=" * 70)
    print("🚀 SUPERSTORE BUSINESS INTELLIGENCE PLATFORM - TEST RUNNER")
    print("=" * 70)
    start_time = time.time()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestDataLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    elapsed = time.time() - start_time
    print("-" * 70)
    print(f"⏱️ Total Execution Time: {elapsed:.3f} seconds")
    print(f"📊 Tests Executed: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    print("=" * 70)

    if result.wasSuccessful():
        print("🎉 ALL TEST CASES PASSED SUCCESSFULLY!")
        return 0
    else:
        print("❌ SOME TEST CASES FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
