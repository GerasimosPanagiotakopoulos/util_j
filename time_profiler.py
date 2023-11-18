import time
import numpy as np
import pandas as pd


class TimeProfiler:

    def __init__(self, silent_mode=False):
        self.silent_mode = silent_mode
        self.all_tasks = []
        self.all_times = []
        return

    def clear(self):
        self.__init__(self.silent_mode)

    def set_silent_mode(self, off=False):
        self.silent_mode = off

    def _task_count(self):
        return len(self.all_tasks)

    def _finish_current_task(self, end_time):
        self.all_times.append(end_time)
        if not self.silent_mode:
            print(f"Finished {self.all_tasks[self._task_count() - 1]}!")

    def new_task(self, task_name):
        current_time = time.time()

        if self._task_count():
            self._finish_current_task(current_time)
        else:
            self.all_times.append(current_time)

        self.all_tasks.append(task_name)

        if not self.silent_mode:
            print(f"{task_name}...")

    def report(self):
        if len(self.all_tasks) == len(self.all_times):  # this will only be False if report() is called consecutively
            self._finish_current_task(time.time())
        if not self.all_tasks:
            return pd.DataFrame(columns=["Task", "Duration", "Total Time"])

        durations = np.diff(self.all_times)
        total_time = np.cumsum(durations)

        return pd.DataFrame({"Task": self.all_tasks, "Duration": durations, "Total Time": total_time})


def main():
    tp = TimeProfiler()
    tp.new_task("Task1")
    time.sleep(5)
    tp.set_silent_mode(True)
    tp.new_task("Task2")
    time.sleep(2)
    tp.set_silent_mode(False)
    tp.new_task("Task3")
    time.sleep(8)
    tp.set_silent_mode(True)
    tp.new_task("Task4")
    time.sleep(4)
    time_report = tp.report()
    print(time_report)
    print(tp.report())
    return

if __name__ == "__main__":
    main()
