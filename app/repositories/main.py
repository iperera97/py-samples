from app.repositories.base import AttendanceRepository
from app.repositories.datafustion.attendance import AttendanceRepository as DataFusionAttendanceRepository


def get_attendance_repo() -> AttendanceRepository:
    return DataFusionAttendanceRepository()
