import re
import json
import math
import time
from consts import BASE_URL, HEADERS, RAW_HERB_DATA_OUTPUT_DIR, RAW_HERB_LIST_OUTPUT, HERB_IDS, LUA_OUTPUT_FILE, HERB_LIST_ENDPOINT
from convert_to_lua import convert_to_lua
from utils import fetch_page_content, setup_logger, save_data_to_json_file, encode_loc

# Set up the logger
logger = setup_logger()

def construct_url(BASE_URL, herb_id, herb_name):
    herb_endpoint = f'object={herb_id}/{herb_name}'
    url = f"{BASE_URL}/{herb_endpoint}"
    logger.info(f"Constructed URL: {url} | Herb ID: {herb_id} | Herb Name: {herb_name}")
    logger.debug(f"URL details: BASE_URL={BASE_URL}, herb_id={herb_id}, herb_name={herb_name}")
    return url

def extract_g_mapper_data(html_content):
    logger.debug("Attempting to extract `g_mapperData` from HTML content.")
    try:
        match = re.search(r'var g_mapperData = ({.*?});', html_content, re.DOTALL)
        if match:
            logger.debug(f"Extracted `g_mapperData`: {match.group(1)[:100]}...")  # Log a snippet for debugging
            return match.group(1).strip()
        else:
            logger.error("Error: `g_mapperData` object not found in the HTML.")
            return None
    except Exception as e:
        logger.error(f"Unexpected error during `g_mapperData` extraction: {e}")
        return None

def fetch_raw_data(output_file_path):
    logger.info(f"Starting fetch_raw_data. Output file: {output_file_path}")
    with open(RAW_HERB_LIST_OUTPUT, 'r', encoding='utf-8') as file:
        herbs = json.load(file)

    total_herbs = len(herbs)
    logger.info(f"Total herbs to process: {total_herbs}")
    processed_herbs = 0

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for herb in herbs:
            herb_id = herb['id']
            herb_name = herb['name']
            logger.info(f"Processing Herb: {herb['displayName']} (ID: {herb_id})")
            logger.debug(f"Herb details: {herb}")

            url = construct_url(BASE_URL, herb_id, herb_name)
            html_content = fetch_page_content(url, HEADERS)
            if not html_content:
                logger.error(f"HTML content retrieval failed for Herb ID: {herb_id} | Herb Name: {herb_name}")
                continue

            raw_data = extract_g_mapper_data(html_content)
            if not raw_data:
                logger.error(f"Data extraction failed for Herb ID: {herb_id} | Herb Name: {herb_name}")
                continue

            logger.debug(f"Raw data for Herb ID {herb_id}: {raw_data[:100]}...")  # Log a snippet of raw data
            output_file.write(json.dumps({"herb_id": herb_id, "herb_name": herb_name, "raw_data": raw_data}) + '\n')
            processed_herbs += 1
            logger.info(f"DONE processing Herb: {herb['displayName']} (ID: {herb_id}) | Processed: {processed_herbs}/{total_herbs}")

    logger.info(f"Finished fetching raw data. Processed herbs: {processed_herbs}/{total_herbs}")

def parse_raw_data(input_file_path, parsed_file_path):
    """
    Parses raw JSON data from an input file, processes it, and writes the corrected data to an output file.

    Args:
        input_file_path (str): The path to the input file containing raw JSON data.
        parsed_file_path (str): The path to the output file where the parsed and corrected data will be saved.

    Raises:
        json.JSONDecodeError: If there is an error parsing JSON data from the input file.

    The function performs the following steps:
        1. Reads raw JSON data line by line from the input file.
        2. Parses each line into a dictionary and extracts the herb name and raw data.
        3. Processes the raw data to correct and organize it by `uiMapId`.
        4. Converts coordinate values from percentages to decimal format.
        5. Maps herb names to herb codes using a predefined dictionary (`HERB_IDS`).
        6. Aggregates the corrected data for each herb.
        7. Writes the aggregated data to the output file in JSON format.

    Logging:
        - Logs the start and end of the parsing process.
        - Logs detailed debug information for each herb being processed.
        - Logs warnings if a herb code is not found for a given herb name.
        - Logs errors if there is an issue parsing JSON data.
    """
    logger.info(f"Starting parse_raw_data. Input file: {input_file_path}, Output file: {parsed_file_path}")
    all_data = {}

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            entry = json.loads(line.strip())
            herb_name = entry['herb_name']
            raw_data = entry['raw_data']
            logger.debug(f"Parsing data for Herb: {herb_name} | Raw Data: {raw_data[:100]}...")

            try:
                parsed_data = json.loads(raw_data)
                corrected_data = {}
                logger.debug(f"Parsed JSON data: {parsed_data}")

                for key, value in parsed_data.items():
                    if isinstance(value, list) and value:
                        ui_map_id = value[0].get("uiMapId")
                        if ui_map_id:
                            corrected_key = str(ui_map_id)
                            if corrected_key in corrected_data:
                                corrected_data[corrected_key].extend(value)
                            else:
                                corrected_data[corrected_key] = value

                for key, value in corrected_data.items():
                    for item in value:
                        if 'coords' in item and isinstance(item['coords'], list):
                            coords_set = {tuple(coord) for coord in item['coords']}
                            item['coords'] = [[round(coord[0] / 100, 4), round(coord[1] / 100, 4)] for coord in coords_set]

                herb_key = herb_name.lower().replace(" ", "-")
                herb_code = HERB_IDS.get(herb_key)
                if herb_code is None:
                    logger.warning(f"No herb_code found for Herb Name: {herb_name} (Key: {herb_key})")

                if herb_name in all_data:
                    all_data[herb_name]['data'].update(corrected_data)
                else:
                    all_data[herb_name] = {
                        "herb_name": herb_name,
                        "herb_code": herb_code,
                        "data": corrected_data
                    }

                logger.debug(f"Corrected data for {herb_name}: {corrected_data}")

            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON for Herb Name: {herb_name} | Error: {e}")

    with open(parsed_file_path, 'w', encoding='utf-8') as output_file:
        for herb_name, entry in all_data.items():
            output_file.write(json.dumps(entry) + '\n')
        logger.info(f"All parsed data successfully saved to {parsed_file_path}")

def extract_herb_list_raw(html_content):
    logger.info("Attempting to extract raw herb list data from HTML content.")
    match = re.search(r'"data":(\[.*?\])(?=,"extraCols")', html_content, re.DOTALL)
    if match:
        logger.info("Successfully extracted raw herb list data.")
        return match.group(1).strip()
    else:
        logger.error("Error: `data` object not found or incomplete in the HTML.")
        return None

def parse_herb_list_raw(raw_data):
    logger.info("Attempting to parse raw herb list data.")
    try:
        herb_list = json.loads(raw_data)
        logger.info("Successfully parsed raw herb list data.")
        for herb in herb_list:
            if 'name' in herb:
                herb['name'] = herb['name'].replace("'", "").lower().replace(" ", "-")
        logger.info("Successfully processed herb list data.")
        return herb_list
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse raw herb list data. Error: {e}")
        return None

def get_herb_list_raw():
    logger.info("Starting to fetch raw herb list data.")
    url = f"{BASE_URL}{HERB_LIST_ENDPOINT}"
    logger.info(f"Fetching HTML content from URL: {url}")

    html_content = fetch_page_content(url, HEADERS)
    if not html_content:
        logger.error("Failed to fetch HTML content for the herb list.")
        return

    logger.debug(f"Fetched HTML content: {html_content[:100]}...")  # Log the first 100 characters for debugging
    raw_data = extract_herb_list_raw(html_content)
    if not raw_data:
        logger.error("Failed to extract raw herb list data from HTML content.")
        return

    logger.debug(f"Extracted raw herb list data: {raw_data[:100]}...")  # Log a snippet of raw data
    parsed_data = parse_herb_list_raw(raw_data)
    if not parsed_data:
        logger.error("Failed to parse raw herb list data.")
        return

    logger.info(f"Saving parsed herb list data to {RAW_HERB_LIST_OUTPUT}")
    save_data_to_json_file(parsed_data, RAW_HERB_LIST_OUTPUT)
    logger.info("Successfully fetched and saved raw herb list data.")
    
def main():
    start_time = time.time()
    print("Starting the main function...This may take a while.")
    print(f"Start time: {time.ctime(start_time)}")
    raw_output_file = RAW_HERB_DATA_OUTPUT_DIR / 'raw.jsonl'
    parsed_output_file = RAW_HERB_DATA_OUTPUT_DIR / 'parsed.jsonl'
    logger.info("Fetching herb list data...")
    print("Fetching herb list data...")
    get_herb_list_raw()
    logger.info("Fetching raw data...")
    print("Fetching raw node location data...")
    fetch_raw_data(raw_output_file)
    logger.info("Parsing raw node location data...")
    print("Parsing raw data...")
    parse_raw_data(raw_output_file, parsed_output_file)
    logger.info("Converting to LUA...")
    print("Converting to LUA...")
    convert_to_lua(parsed_output_file, LUA_OUTPUT_FILE)
    total_time = time.time() - start_time
    logger.info(f"Total time taken: {total_time:.2f} seconds")
    print("All done!")
    print(f"End time: {time.ctime()} | Total time taken: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
