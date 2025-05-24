import os
import sys
from pathlib import Path
from loguru import logger

def setup_logger():
    """Configure the application logger."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure loguru
    config = {
        "handlers": [
            {"sink": sys.stderr, "level": "INFO"},
            {"sink": logs_dir / "app.log", "rotation": "10 MB", "level": "DEBUG"},
        ],
        "extra": {"user": "unknown"},
    }
    
    # Remove default handler
    logger.remove()
    
    # Add handlers from config
    for handler in config["handlers"]:
        logger.add(**handler)
    
    logger.info("Logger initialized")
    
    return logger