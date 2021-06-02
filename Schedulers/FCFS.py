from Schedulers.Base import BaseScheduler


class FCFS(BaseScheduler):

    def __init__(self):
        super().__init__()

    def add_to_ready(self):
        for task in self.ready_queue:
            task.acquire_lock_for_resourses()
            self.check_and_add_task_to_cpus(task)
            task.release_lock_for_resourses()
        self.ready_queue = []

    def add_from_waiting(self):
        list = []
        for i in range(len(self.waiting_queue)):
            self.waiting_queue[i].acquire_lock_for_resourses()
            if self.waiting_queue[i].is_resources_available():
                self.ready_queue.append(self.waiting_queue[i])
                list.append(self.waiting_queue[i])
            self.waiting_queue[i].release_lock_for_resourses()

        for item in list:
            self.waiting_queue.remove(item)

    def start(self):
        self.print_task()
        while self.ready_queue or self.waiting_queue:
            self.add_from_waiting()
            self.add_to_ready()



