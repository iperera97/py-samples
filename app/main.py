import logging

from flask import Flask, jsonify

from app.api.attendance import attendance_bp
from app.exceptions import RepositoryError

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(attendance_bp)

    @app.errorhandler(RepositoryError)
    def handle_repository_error(e: RepositoryError):
        logger.error("repository error: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(e: Exception):
        logger.error("unhandled error: %s", e, exc_info=True)
        return jsonify({"error": "internal server error"}), 500

    return app


app = create_app()
