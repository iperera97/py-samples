from unittest.mock import patch
import pandas as pd
import pytest

from app.exceptions import RepositoryError
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


@patch("app.repositories.datafustion.base.AmazonS3")
def test_get_attendance_trend_wraps_query_failure(mock_s3, mock_ctx):
    mock_ctx.sql.return_value.to_pandas.side_effect = ValueError("query failed")
    repo = AttendanceRepository()

    with pytest.raises(RepositoryError) as exc_info:
        repo.get_attendance_trend(days=30)

    assert isinstance(exc_info.value.cause, ValueError)
    assert mock_ctx.sql.return_value.to_pandas.call_count == 3
