import logging

from flask import Blueprint, jsonify, request

from app.repositories.main import get_attendance_repo
from app.services.attendance import AttendanceService

logger = logging.getLogger(__name__)
attendance_bp = Blueprint("attendance", __name__, url_prefix="/api/attendance")


def _get_service() -> AttendanceService:
    repo = get_attendance_repo()
    return AttendanceService(repo)


@attendance_bp.route("/trend", methods=["GET"])
def attendance_trend():
    days = request.args.get("days", default=30, type=int)
    service = _get_service()
    data = service.get_attendance_trend(days)
    return jsonify({"data": data}), 200


@attendance_bp.route("/count", methods=["GET"])
def attendance_count():
    days = request.args.get("days", default=30, type=int)
    service = _get_service()
    data = service.get_attendance_count(days)
    return jsonify({"data": data}), 200
