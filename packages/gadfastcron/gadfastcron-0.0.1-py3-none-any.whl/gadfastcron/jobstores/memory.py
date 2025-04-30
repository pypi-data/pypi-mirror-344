from apscheduler.jobstores.memory import MemoryJobStore


class Memory:
    def __init__(self) -> None:
        self.store = MemoryJobStore()
