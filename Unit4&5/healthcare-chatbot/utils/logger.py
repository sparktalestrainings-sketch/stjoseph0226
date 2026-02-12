"""
utils/logger.py - Simple logging
"""

import logging
import json
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "medassist.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("medassist")


def log_query(user: str, answer: str, session_id: str = "", provider: str = "", model: str = ""):
    """Log a query interaction."""
    try:
        logger.info(json.dumps({
            "ts": datetime.utcnow().isoformat(),
            "session": session_id,
            "provider": provider,
            "model": model,
            "user": user[:200],
            "answer": answer[:400],
        }))
    except Exception:
        pass


def log_error(err: Exception, ctx: str = ""):
    """Log an error."""
    try:
        logger.error(json.dumps({
            "ts": datetime.utcnow().isoformat(),
            "error": str(err),
            "context": ctx,
        }))
    except Exception:
        pass
