import logging

from app.exceptions import RepositoryError, ServiceError
from app.repositories.base import AttendanceRepository

logger = logging.getLogger(__name__)


class AttendanceService:
    def __init__(self, repo: AttendanceRepository):
        self._repo = repo

    def get_attendance_trend(self, days: int = 30) -> list[dict]:
        try:
            df = self._repo.get_attendance_trend(days)
            return df.to_dict(orient="records")
        except RepositoryError as e:
            logger.error("get_attendance_trend failed: %s", e, exc_info=True)
            raise ServiceError("failed to get attendance trend", cause=e) from e

    def get_attendance_count(self, days: int = 30) -> int:
        try:
            return self._repo.get_attendance_count(days)
        except RepositoryError as e:
            logger.error("get_attendance_count failed: %s", e, exc_info=True)
            raise ServiceError("failed to get attendance count", cause=e) from e
