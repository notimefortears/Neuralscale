import logging
import os

def setup_logging(service_name: str) -> logging.Logger:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format=f"%(asctime)s | {service_name} | %(levelname)s | %(message)s",
    )
    return logging.getLogger(service_name)
