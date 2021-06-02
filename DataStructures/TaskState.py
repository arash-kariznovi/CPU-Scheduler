import enum


class State(enum.Enum):
    ready = 1
    waiting = 2
    running = 3


class Priority(enum.Enum):
    low = 3
    med = 2
    high = 1
