import requests
import json
import math

from logging_config import setup_logger


# Set up the logger
logger = setup_logger()


def fetch_page_content(url, HEADERS, timeout=10):
    """
    Fetch the content of a page using the provided URL and headers.
    """
    logger.info(f"Fetching content from URL: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        logger.info(f"Response received with status code: {response.status_code}")
        if response.status_code == 200:
            return response.text
        logger.error(f"Failed to fetch page content. HTTP {response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None


def save_data_to_json_file(data, file_path, ensure_ascii=False):
    """
    Save data to a JSON file.
    """
    logger.info(f"Saving data to file: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=ensure_ascii)
        logger.info(f"Data successfully saved to {file_path}")
    except IOError as e:
        logger.error(f"Failed to save data to {file_path}. Error: {e}")
    
def encode_loc(x, y):
    if x > 0.9999:
        x = 0.9999
    if y > 0.9999:
        y = 0.9999
    return math.floor(x * 10000 + 0.5) * 1000000 + math.floor(y * 10000 + 0.5) * 100


