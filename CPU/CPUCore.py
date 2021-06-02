import time
from threading import Thread, Lock

from DataStructures.Timer import Timer


class CPUCore:

    def __init__(self, core_name):
        self.core_name = core_name
        self.task = None
        self.executing_task_id = -1
        self.idle_time = 0
        self.idle_timer = Timer()
        self.idle_timer.start()
        self.worked_time = 0
        self.working_lock = Lock()

    def get_task_count(self):
        return len(self.task)

    def add_task(self, task):
        self.idle_time += self.idle_timer.stop()
        self.task = task
        self.executing_task_id = task.id
        task.needed_resources[0].in_use += 1
        task.needed_resources[1].in_use += 1
        single_thread = Thread(target=self.runnable_task, args=(task,))
        single_thread.start()

    def runnable_task(self, task):

        # print(self.core_name + ' executing task with name: ' + task.name, end='\n')
        time.sleep(task.executing_time)
        self.executing_task_id = -1
        self.idle_timer.start()

        task.acquire_lock_for_resourses()
        task.needed_resources[0].in_use -= 1
        task.needed_resources[1].in_use -= 1
        task.release_lock_for_resourses()

    def get_idle_time(self):
        return self.core_name + ' idle-time: ' + str(round(self.idle_time) + round(self.idle_timer.stop()))

    def __str__(self):
        if self.executing_task_id != -1:
            return self.core_name + ' executing task with name: ' + self.task.name
        else:
            return self.core_name + ' idle '
