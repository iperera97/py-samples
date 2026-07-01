import pandas as pd

from app.constants import ATTENDANCE_S3_BUCKET
from app.repositories.base import AttendanceRepository as AttendanceRepositoryInterface
from app.repositories.datafustion.base import DataFusionBaseRepository


class AttendanceRepository(DataFusionBaseRepository, AttendanceRepositoryInterface):
    def __init__(self):
        super().__init__()
        self._ctx.register_parquet("attendance", f"s3://{ATTENDANCE_S3_BUCKET}/attendance.parquet")

    def get_attendance_trend(self, days: int) -> pd.DataFrame:
        sql = f"""
            SELECT date_trunc('day', attendance_date) AS day,
                   COUNT(*) FILTER (WHERE status = 'present') AS present_count,
                   COUNT(*) AS total_count
            FROM attendance
            WHERE attendance_date >= now() - INTERVAL '{days} days'
            GROUP BY 1
            ORDER BY 1
        """
        return self._run_query(sql)

    def get_attendance_count(self, days: int) -> int:
        sql = f"""
            SELECT COUNT(*) AS total_count
            FROM attendance
            WHERE attendance_date >= now() - INTERVAL '{days} days'
        """
        df = self._run_query(sql)
        return int(df["total_count"].iloc[0])
