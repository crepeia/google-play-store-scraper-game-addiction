import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google_play_scraper import Sort, reviews

from utils import (create_list_of_app_ids,
	fetch_most_relevants_comments_all_apks,
	read_files_in_folder, 
	store_apps_from_category,
        fetch_and_store_comments,
        fetch_and_store_comments_all_apks)

CATEGORIES = {
    "GAME_ACTION": "GAME_ACTION",
    "GAME_ADVENTURE": "GAME_ADVENTURE",
    "GAME_ARCADE": "GAME_ARCADE",
    "GAME_BOARD": "GAME_BOARD",
    "GAME_CARD": "GAME_CARD",
    "GAME_CASINO": "GAME_CASINO",
    "GAME_CASUAL": "GAME_CASUAL",
    "GAME_PUZZLE": "GAME_PUZZLE",
    "GAME_RACING": "GAME_RACING",
    "GAME_ROLE_PLAYING": "GAME_ROLE_PLAYING",
    "GAME_SIMULATION": "GAME_SIMULATION",
    "GAME_SPORTS": "GAME_SPORTS",
    "GAME_STRATEGY": "GAME_STRATEGY",
    "GAME_TRIVIA": "GAME_TRIVIA",
    "GAME_WORD": "GAME_WORD",
}

# Run once
#for category in CATEGORIES:
#    store_apps_from_category(category)
data = create_list_of_app_ids()
data = data[data['rank'] < 11]
app_id_list = data['app_id']

# Create folder for each app_id
# Run once 
# MOST_RELEVANT
#fetch_most_relevants_comments_all_apks(app_id_list)

# Store and update data from newest reviews
# NEWEST
fetch_and_store_comments_all_apks(app_id_list)
