import unittest
from time_profiler import TimeProfiler
import io
import sys
import time

class TestTimeProfiler(unittest.TestCase):

    def setUp(self):
        # Redirect stdout
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self):
        # Reset stdout
        sys.stdout = sys.__stdout__

    def test_initialization(self):
        tp = TimeProfiler()
        self.assertEqual(tp._task_count(), 0)
        self.assertFalse(tp.silent_mode)

    def test_new_task(self):
        tp = TimeProfiler()
        tp.new_task("Test Task")
        self.assertEqual(tp._task_count(), 1)

    def test_report_generation(self):
        tp = TimeProfiler()

        tp.new_task("Task 1")
        time.sleep(0.5)
        tp.new_task("Task 2")
        time.sleep(1)
        tp.new_task("Task 3")
        time.sleep(0.7)

        report = tp.report()
        self.assertAlmostEqual(report.loc[report['Task'] == 'Task 1', 'Duration'].iloc[0], 0.5, delta=0.01)
        self.assertAlmostEqual(report.loc[report['Task'] == 'Task 2', 'Duration'].iloc[0], 1.0, delta=0.01)
        self.assertAlmostEqual(report.loc[report['Task'] == 'Task 3', 'Duration'].iloc[0], 0.7, delta=0.01)

        self.assertAlmostEqual(report.loc[report['Task'] == 'Task 1', 'Total Time'].iloc[0], 0.5, delta=0.01)
        self.assertAlmostEqual(report.loc[report['Task'] == 'Task 2', 'Total Time'].iloc[0], 1.5, delta=0.01)
        self.assertAlmostEqual(report.loc[report['Task'] == 'Task 3', 'Total Time'].iloc[0], 2.2, delta=0.01)

    def test_silent_mode_on(self):
        tp = TimeProfiler(silent_mode=True)
        tp.new_task("SilentTask")
        tp.report()
        self.assertEqual(self.capturedOutput.getvalue(), '')

    def test_silent_mode_off(self):
        tp = TimeProfiler(silent_mode=False)
        tp.new_task("LoudTask")
        tp.report()
        self.assertIn("LoudTask...", self.capturedOutput.getvalue())
        self.assertIn("Finished LoudTask!", self.capturedOutput.getvalue())


if __name__ == '__main__':
    unittest.main()
