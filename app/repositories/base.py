from abc import ABC, abstractmethod

import pandas as pd


class AttendanceRepository(ABC):
    @abstractmethod
    def get_attendance_trend(self, days: int) -> pd.DataFrame:
        ...

    @abstractmethod
    def get_attendance_count(self, days: int) -> int:
        ...
