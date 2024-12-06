# Herb Data Processing Project

Python project designed to fetch, parse, and convert data about herbs and their locations from a web source into LUA format for use in applications like GatherMate2. The project is released under an open-source license, encouraging contributions, adaptations, and community improvements.

## Features

- **Data Fetching**: Scrapes herb-related data from a specified web source.  
- **Raw Data Processing**: Structures and organizes extracted data into JSON format.  
- **Data Parsing**: Refines raw data with corrected coordinates and herb mappings.  
- **LUA Conversion**: Outputs parsed data into LUA format compatible with GatherMate2.  
- **Logging**: Detailed logging for transparency and ease of debugging.  

## Project Structure

- main.py: Manages the end-to-end data processing workflow.  
- utils.py: Contains helper functions for web scraping and file handling.  
- consts.py: Holds constants and configurations for the project.  
- logging_config.py: Implements custom JSON-based logging.  

## Requirements

### Python Version
Python 3.8+

### Dependencies
Install dependencies using:

pip install -r requirements.txt

#### Required Libraries
- requests: For HTTP requests.  
- logging: For generating logs.  
- json: For JSON handling.  
- re: For parsing with regular expressions.  

## Setup

### Clone the repository
git clone <repository_url>  
cd <repository_directory>  

### Prepare necessary directories
data/raw/lists/  
data/raw/herbs_data/  
data/output/  

### Update configuration
Modify BASE_URL, endpoints, and headers as needed in consts.py.

## Usage

Run the script with:

python main.py

### Outputs
- **Raw Herb List**: data/raw/lists/raw_herb_list.json  
- **Raw Herb Data**: data/raw/herbs_data/raw.jsonl  
- **Parsed Data**: data/raw/herbs_data/parsed.jsonl  
- **LUA File**: data/output/HerbDataYYYYMMDD.lua  

### Logs
Logs are saved in the logs/ directory:  
- **Debug Logs**: Detailed logs for debugging (debug.log).  
- **Info Logs**: High-level process logs (info.log).  
