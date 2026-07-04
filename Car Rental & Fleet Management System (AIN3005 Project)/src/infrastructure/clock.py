from abc import ABC, abstractmethod
from datetime import datetime

class AbstractClock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass

class SystemClock(AbstractClock):
    def now(self) -> datetime:
        return datetime.now()

class FixedClock(AbstractClock):
    def __init__(self, fixed_time: datetime):
        self._time = fixed_time

    def now(self) -> datetime:
        return self._time