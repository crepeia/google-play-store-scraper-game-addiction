import time
import os
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
        fetch_most_relevant_comments,
        fetch_and_store_comments,
        fetch_and_store_comments_all_apks)

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
