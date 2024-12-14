import logging

def setup_logging():
    """Configure consistent logging across all modules"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
