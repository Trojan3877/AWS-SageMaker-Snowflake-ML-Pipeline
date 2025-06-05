# src/utils.py

"""
Utilities Module
----------------
Common utility functions (logging, saving outputs, etc.)
"""

import logging

def setup_logger():
    """
    Sets up a basic logger.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    return logger
