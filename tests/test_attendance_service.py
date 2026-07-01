from unittest.mock import Mock

import pandas as pd
import pytest

from app.exceptions import RepositoryError, ServiceError
from app.services.attendance import AttendanceService


def test_get_attendance_trend_returns_list_of_dicts():
    mock_repo = Mock()
    mock_repo.get_attendance_trend.return_value = pd.DataFrame(
        [{"day": "2026-06-30", "present_count": 28, "total_count": 30}]
    )
    service = AttendanceService(mock_repo)

    result = service.get_attendance_trend(days=7)

    assert result == [{"day": "2026-06-30", "present_count": 28, "total_count": 30}]
    mock_repo.get_attendance_trend.assert_called_once_with(7)


def test_get_attendance_trend_wraps_repository_error():
    mock_repo = Mock()
    mock_repo.get_attendance_trend.side_effect = RepositoryError("boom")
    service = AttendanceService(mock_repo)

    with pytest.raises(ServiceError) as exc_info:
        service.get_attendance_trend(days=7)

    assert isinstance(exc_info.value.cause, RepositoryError)
