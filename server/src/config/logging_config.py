import os
import logging
from logging.handlers import RotatingFileHandler
from server.src.config.config import Config

def setup_logger(app_name: str = "siredo-server", log_level: str = None) -> logging.Logger:
    level_name = log_level or Config.LOG_LEVEL
    log_level_val = getattr(logging, level_name.upper(), logging.INFO)
    
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level_val)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z"
        )
        
        # 1. Dedicated File Handler (Rotating File Handler: max 10MB, 5 backups)
        try:
            log_file = Config.LOG_FILE
            os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level_val)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass

        # 2. Console Error Handler (Only warnings & errors to stderr for clean terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()
