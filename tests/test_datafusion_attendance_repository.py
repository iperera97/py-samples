from unittest.mock import patch
import pandas as pd
import pytest

from app.repositories.datafustion.attendance import AttendanceRepository


@pytest.fixture
def mock_ctx():
    with patch("app.repositories.datafustion.base.SessionContext") as mock_ctx_cls:
        yield mock_ctx_cls.return_value


@patch("app.repositories.datafustion.base.AmazonS3")
def test_get_attendance_trend_success(mock_s3, mock_ctx):
    mock_ctx.sql.return_value.to_pandas.return_value = "df_result"
    repo = AttendanceRepository()

    result = repo.get_attendance_trend(days=30)

    assert result == "df_result"
    mock_ctx.register_object_store.assert_called_once()
    mock_ctx.register_parquet.assert_called_once()


@patch("app.repositories.datafustion.base.AmazonS3")
def test_get_attendance_count_success(mock_s3, mock_ctx):
    mock_ctx.sql.return_value.to_pandas.return_value = pd.DataFrame([{"total_count": 42}])
    repo = AttendanceRepository()

    result = repo.get_attendance_count(days=30)

    assert result == 42
