import logging

def setup_logger():
    """
    Sets up a logger for the application.
    :return: Configured logger instance.
    """
    logger = logging.getLogger("StockScraper")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
