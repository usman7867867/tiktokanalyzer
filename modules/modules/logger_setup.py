"""Logging setup module."""
import logging
import os

def setup_logging(log_file='data/app.log', log_level='INFO'):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger('USMAN_TikTok')
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # File handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(file_formatter)

    # Console handler (only errors)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    ch.setFormatter(console_formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
