from Schedulers.Base import BaseScheduler


class SJF(BaseScheduler):

    def __init__(self):
        super().__init__()

    def add_to_ready(self):
        for task in self.ready_queue:
            task.acquire_lock_for_resourses()
            self.check_and_add_task_to_cpus(task)
            task.release_lock_for_resourses()

        self.ready_queue = []

    def add_from_waiting(self):
        temp_list = []

        for task in self.waiting_queue:
            task.acquire_lock_for_resourses()
            if task.is_resources_available():
                self.ready_queue.append(task)
                temp_list.append(task)
            task.release_lock_for_resourses()

        for item in temp_list:
            self.waiting_queue.remove(item)

    def start(self):
        self.sort_by_burstTime()
        self.print_task()
        while self.ready_queue or self.waiting_queue:
            self.add_from_waiting()

            self.add_to_ready()

    def sort_by_burstTime(self):
        low = 0
        high = len(self.ready_queue) - 1
        self.quickSort(low, high)

    def quickSort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quickSort(low, pi - 1)
            self.quickSort(pi + 1, high)

    def partition(self, low, high):
        i = (low - 1)
        pivot = self.ready_queue[high].executing_time

        for j in range(low, high):
            if self.ready_queue[j].executing_time < pivot:
                i = i + 1
                self.ready_queue[i], self.ready_queue[j] = self.ready_queue[j], self.ready_queue[i]

        self.ready_queue[i + 1], self.ready_queue[high] = self.ready_queue[high], self.ready_queue[i + 1]
        return i + 1
