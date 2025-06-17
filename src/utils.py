import logging
import os
import pandas as pd
import json
from datetime import datetime

from . import config

def setup_logging():
    """Sets up the logging configuration."""
    log_dir = os.path.join(os.path.dirname(__file__), config.LOG_DIR)
    os.makedirs(log_dir, exist_ok=True)
    log_filepath = os.path.join(log_dir, config.LOG_FILENAME)

    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler() # Also print logs to console
        ]
    )
    logging.info("Logging setup complete.")

def save_to_csv(data, filename):
    """Saves the scraped data to a CSV file.

    Args:
        data (list): A list of dictionaries, where each dictionary represents a job posting.
        filename (str): The name of the output CSV file.
    """
    output_dir = os.path.join(os.path.dirname(__file__), config.OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    if not data:
        logging.warning("No data provided to save to CSV.")
        return

    try:
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding="utf-8")
        logging.info(f"Data successfully saved to {filepath}")
    except Exception as e:
        logging.error(f"Error saving data to CSV {filepath}: {e}")

def save_to_json(data, filename):
    """Saves the scraped data to a JSON file.

    Args:
        data (list): A list of dictionaries, where each dictionary represents a job posting.
        filename (str): The name of the output JSON file.
    """
    output_dir = os.path.join(os.path.dirname(__file__), config.OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    if not data:
        logging.warning("No data provided to save to JSON.")
        return

    try:
        with open(filepath, \'w\', encoding=\'utf-8\') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Data successfully saved to {filepath}")
    except Exception as e:
        logging.error(f"Error saving data to JSON {filepath}: {e}")

def get_timestamp_string():
    """Returns the current timestamp as a string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


