import os

API_KEY = os.getenv('API_KEY', '')
API_HOST = os.getenv('API_HOST', 'https://observa-server.steamory.com')
OUTPUT_LOG_SWITCH = os.getenv('OUTPUT_LOG_SWITCH', 'false').lower() == 'true'
PROJECT_ID = os.getenv('PROJECT_ID', '')
