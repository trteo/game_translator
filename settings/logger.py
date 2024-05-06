from loguru import logger

from settings.config import BASE_DIR

log_dir = BASE_DIR / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
logger.add(sink=log_dir / "translation_logs.log", rotation="10 MB", retention="10 days", level="DEBUG")
