import logging
import sys
from pathlib import Path
from src.config import LOGS_DIR

def setup_logger(name: str, log_file: str = "app.log", level=logging.INFO):
    """Function to setup a logger with file and console handlers"""
    
    # Create logs directory if it doesn't exist (redundant with config but safe)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
    
    log_path = LOGS_DIR / log_file
    
    # File Handler
    try:
        handler = logging.FileHandler(log_path)        
        handler.setFormatter(formatter)
    except Exception as e:
        print(f"Failed to create log file handler: {e}")
        handler = logging.NullHandler()

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    
    # Prevent adding handlers multiple times if logger is retrieved again
    if not logger.handlers:
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.addHandler(console_handler)
    
    return logger

# Create default loggers
# app_logger: General application events
app_logger = setup_logger("app_logger", "app.log")

# rag_logger: Detailed RAG traces, retrieval results, prompts
rag_logger = setup_logger("rag_logger", "rag_debug.log", level=logging.DEBUG)
