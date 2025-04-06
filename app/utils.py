import logging
import os

def configure_logging():
    log_file = os.getenv("LOG_FILE", "app.log")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

logger = configure_logging()