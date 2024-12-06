from pathlib import Path
from datetime import datetime

TODAYS_DATE = datetime.today().strftime('%Y%m%d')

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / 'src'
# Logs directory
LOGS_DIR = SRC_DIR / 'logs'

#output directories
OUTPUT_DIR = BASE_DIR / 'data' / 'output'
LUA_OUTPUT_FILE = OUTPUT_DIR / f'HerbData{TODAYS_DATE}.lua'

# Raw data directories and files
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
RAW_LISTS_DIR = RAW_DATA_DIR / 'lists'
RAW_HERB_LIST_OUTPUT = RAW_LISTS_DIR / 'raw_herb_list.json'
RAW_ZONE_LIST_OUTPUT = RAW_LISTS_DIR / 'raw_zone_list.json'
RAW_HERB_DATA_OUTPUT_DIR = RAW_DATA_DIR / 'herbs_data'
RAW_TEMP_DATA_DIR = RAW_DATA_DIR / 'temp'
HERB_PARSED_JSONL = RAW_HERB_DATA_OUTPUT_DIR / 'parsed.jsonl'

# Data dictionaries locations
ZONE_DICT = RAW_DATA_DIR / 'ref' / 'zone_dict.json'

# Request constants
BASE_URL = 'https://www.wowhead.com'
HERB_LIST_ENDPOINT = '/objects/herbs?filter=17;11;0'
ZONE_LIST_ENDPOINT = '/zones'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

HERB_DICT_SCHEMA = {
    
    "id": "int",
    "displayName": "str",
    "name": "str"
}

ZONE_DICT_SCHEMA = {
        "uiMapName": "str",
        "uiMapId ": "int",
        "wow-head_zone_id": "int",
}

# Got this from GatherMate2 addon
HERB_IDS = {
    "mycobloom": 1439,
    "lush-mycobloom": 1440,
    "irradiated-mycobloom": 1441,
    "sporefused-mycobloom": 1442,
    "sporelusive-mycobloom": 1443,
    "crystallized-mycobloom": 1444,
    "altered-mycobloom": 1445,
    "camouflaged-mycobloom": 1446,
    "blessing-blossom": 1447,
    "lush-blessing-blossom": 1448,
    "irradiated-blessing-blossom": 1449,
    "sporefused-blessing-blossom": 1450,
    "sporelusive-blessing-blossom": 1451,
    "crystallized-blessing-blossom": 1452,
    "altered-blessing-blossom": 1453,
    "camouflaged-blessing-blossom": 1454,
    "luredrop": 1455,
    "lush-luredrop": 1456,
    "irradiated-luredrop": 1457,
    "sporefused-luredrop": 1458,
    "sporelusive-luredrop": 1459,
    "crystallized-luredrop": 1460,
    "altered-luredrop": 1461,
    "camouflaged-luredrop": 1462,
    "orbinid": 1463,
    "lush-orbinid": 1464,
    "irradiated-orbinid": 1465,
    "sporefused-orbinid": 1466,
    "sporelusive-orbinid": 1467,
    "crystallized-orbinid": 1468,
    "altered-orbinid": 1469,
    "camouflaged-orbinid": 1470,
    "arathors-spear": 1471,
    "lush-arathors-spear": 1472,
    "irradiated-arathors-spear": 1473,
    "sporefused-arathors-spear": 1474,
    "sporelusive-arathors-spear": 1475,
    "crystallized-arathors-spear": 1476,
    "altered-arathors-spear": 1477,
    "camouflaged-arathors-spear": 1478
}
