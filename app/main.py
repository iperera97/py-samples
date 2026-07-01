import logging

from flask import Flask, jsonify

from app.api.attendance import attendance_bp
from app.exceptions import ServiceError

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(attendance_bp)
    _register_error_handlers(app)
    return app


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ServiceError)
    def handle_service_error(e: ServiceError):
        logger.error("service error: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(e: Exception):
        logger.error("unhandled error: %s", e, exc_info=True)
        return jsonify({"error": "internal server error"}), 500


app = create_app()
