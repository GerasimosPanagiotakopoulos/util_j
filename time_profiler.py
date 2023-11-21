import time
import numpy as np
import pandas as pd


class TimeProfiler:

    def __init__(self, silent_mode=False):
        """
        Initializes the TimeProfiler instance.

        Parameters:
        silent_mode (bool): If True, suppresses print statements for task start and finish. Defaults to False.
        """
        self.silent_mode = silent_mode
        self.all_tasks = []
        self.all_times = []
        return


    def clear(self):
        """
        Resets the profiler by reinitializing all attributes. Keeps the silent mode as is.
        """
        self.__init__(self.silent_mode)

    def switch_silent_mode(self, off=False):
        """
        Toggles the silent mode.

        Parameters:
        off (bool): If True, turns off silent mode. If False, turns on silent mode.
        """
        self.silent_mode = off

    def _task_count(self):
        """
        Returns the number of tasks that have been added.

        This method is intended for internal use.

        Returns:
        int: Number of tasks.
        """

    def _finish_current_task(self, end_time):
        """
        Marks the current task as finished and records its end time.

        This method is intended for internal use.

        Parameters:
        current_time (float): The end time of the current task.
        """
        self.all_times.append(end_time)
        if not self.silent_mode:
            print(f"Finished {self.all_tasks[self._task_count() - 1]}!")

    def new_task(self, task_name):
        """
        Starts a new task. If there is an ongoing task, it finishes that task before starting the new one.

        Parameters:
        task_name (str): The name of the new task.
        """
        current_time = time.time()

        if self._task_count():
            self._finish_current_task(current_time)
        else:
            self.all_times.append(current_time)

        self.all_tasks.append(task_name)

        if not self.silent_mode:
            print(f"{task_name}...")

    def report(self):
        """
        Finalizes the current task, calculates, and returns a report of all tasks as a DataFrame.

        Returns:
        pandas.DataFrame: A DataFrame containing the duration and total time of each task.
        """
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
