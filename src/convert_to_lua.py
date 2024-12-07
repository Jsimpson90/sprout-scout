import json

from utils import setup_logger, encode_loc

logger = setup_logger()


def convert_to_lua(parsed_file_path, lua_output_file):
    logger.info(f"Starting LUA conversion. Input file: {parsed_file_path}, Output file: {lua_output_file}")
    gathermate_db = {}

    with open(parsed_file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                logger.debug(f"Processing data: {data}")
                herb_code = data.get('herb_code')
                if not herb_code:
                    continue
                nested_data = data.get('data', {})
                for map_id, map_details in nested_data.items():
                    for map_entry in map_details:
                        coords = map_entry.get('coords', [])
                        ui_map_id = map_entry.get('uiMapId')
                        if not (ui_map_id and coords):
                            continue
                        for coord in coords:
                            encoded_location = encode_loc(*coord)
                            if ui_map_id not in gathermate_db:
                                gathermate_db[ui_map_id] = {}
                            gathermate_db[ui_map_id][encoded_location] = herb_code
            except Exception as e:
                logger.error(f"Error processing line: {line}, Error: {e}")

    with open(lua_output_file, 'w') as f:
        f.write("GatherMate2HerbDB = {\n")
        for map_id, locations in gathermate_db.items():
            f.write(f"    [{map_id}] = {{\n")
            for loc, herb in locations.items():
                f.write(f"        [{loc}] = {herb},\n")
            f.write("    },\n")
        f.write("}\n")
    logger.info(f"LUA file written: {lua_output_file}")