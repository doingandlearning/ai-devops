import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from flask import Flask

from .config import AppSettings
from .routes import bp as routes_bp


def create_app() -> Flask:
	settings = AppSettings()  # loads from environment
	app = Flask(__name__)

	# Basic config exposure (avoid secrets)
	app.config["ENV_NAME"] = settings.env_name

	# Configure logging
	log_level = logging.DEBUG if settings.env_name == "dev" else logging.INFO
	log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	
	# Create logs directory if it doesn't exist
	log_dir = Path("logs")
	log_dir.mkdir(exist_ok=True)
	
	# Log file path
	log_file = log_dir / "slackbot.log"
	
	# Configure root logger
	root_logger = logging.getLogger()
	root_logger.setLevel(log_level)
	
	# Remove existing handlers to avoid duplicates
	root_logger.handlers.clear()
	
	# File handler with rotation (10MB max, keep 5 backups)
	file_handler = RotatingFileHandler(
		log_file,
		maxBytes=10 * 1024 * 1024,  # 10MB
		backupCount=5,
		encoding='utf-8'
	)
	file_handler.setLevel(log_level)
	file_handler.setFormatter(logging.Formatter(log_format))
	root_logger.addHandler(file_handler)
	
	# Console handler (stdout)
	console_handler = logging.StreamHandler()
	console_handler.setLevel(log_level)
	console_handler.setFormatter(logging.Formatter(log_format))
	root_logger.addHandler(console_handler)
	
	logging.info(f"Logging configured - Level: {logging.getLevelName(log_level)}, File: {log_file}")

	# Register routes
	app.register_blueprint(routes_bp)

	return app


def main() -> None:
	app = create_app()
	# Default to port 8000 if not provided
	app.run(host="0.0.0.0", port=AppSettings().port)


if __name__ == "__main__":
	main()
