import requests
import json
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


# Example usage in the main script:
if __name__ == "__main__":
    # Example URL and headers
    example_url = "https://example.com/api/data"
    example_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Fetch page content
    content = fetch_page_content(example_url, example_headers)
    if content:
        # Process and save content (assuming `content` is already JSON-compatible)
        example_data = json.loads(content)  # Example: processing raw content
        save_data_to_json_file(example_data, "output.json")


