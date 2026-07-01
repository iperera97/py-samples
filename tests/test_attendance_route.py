from unittest.mock import Mock, patch

import pytest

from app.exceptions import ServiceError
from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


@patch("app.api.attendance._get_service")
def test_attendance_trend_returns_200(mock_get_service, client):
    mock_service = Mock()
    mock_service.get_attendance_trend.return_value = [{"day": "2026-06-30", "present_count": 28}]
    mock_get_service.return_value = mock_service

    resp = client.get("/api/attendance/trend?days=7")

    assert resp.status_code == 200
    assert resp.get_json() == {"data": [{"day": "2026-06-30", "present_count": 28}]}
    mock_service.get_attendance_trend.assert_called_once_with(7)


@patch("app.api.attendance._get_service")
def test_attendance_trend_returns_500_on_service_error(mock_get_service, client):
    mock_service = Mock()
    mock_service.get_attendance_trend.side_effect = ServiceError("db down")
    mock_get_service.return_value = mock_service

    resp = client.get("/api/attendance/trend")

    assert resp.status_code == 500
    assert resp.get_json() == {"error": "db down"}


@patch("app.api.attendance._get_service")
def test_attendance_count_returns_200(mock_get_service, client):
    mock_service = Mock()
    mock_service.get_attendance_count.return_value = 42
    mock_get_service.return_value = mock_service

    resp = client.get("/api/attendance/count?days=7")

    assert resp.status_code == 200
    assert resp.get_json() == {"data": 42}
