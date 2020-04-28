import glob
import logging
import time
import random
import os

import numpy as np
import pandas as pd
import play_scraper
import requests
from bs4 import BeautifulSoup
from google_play_scraper import Sort, reviews

logging.basicConfig(
        filename='var/log.log',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

class HTMLTableParser:
       
        def parse_url(self, url):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            return [(table['id'],self.parse_html_table(table))\
                    for table in soup.find_all('table')]  
    
        def parse_html_table(self, table):
            n_columns = 0
            n_rows=0
            column_names = []
    
            # Find number of rows and columns
            # we also find the column titles if we can
            for row in table.find_all('tr'):
                
                # Determine the number of rows in the table
                td_tags = row.find_all('td')
                if len(td_tags) > 0:
                    n_rows+=1
                    if n_columns == 0:
                        # Set the number of columns for our table
                        n_columns = len(td_tags)
                        
                # Handle column names if we find them
                th_tags = row.find_all('th') 
                if len(th_tags) > 0 and len(column_names) == 0:
                    for th in th_tags:
                        column_names.append(th.get_text())
    
            # Safeguard on Column Titles
            if len(column_names) > 0 and len(column_names) != n_columns:
                raise Exception("Column titles do not match the number of columns")
    
            columns = column_names if len(column_names) > 0 else range(0,n_columns)
            df = pd.DataFrame(columns = columns,
                              index= range(0,n_rows))
            row_marker = 0
            for row in table.find_all('tr'):
                column_marker = 0
                columns = row.find_all('td')
                for column in columns:
                    df.iat[row_marker,column_marker] = column.get_text()
                    column_marker += 1
                if len(columns) > 0:
                    row_marker += 1
                    
            # Convert to float if possible
            for col in df:
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass
            
            return df

def store_apps_from_category(category):
    try:
        URL = r'https://www.androidrank.org/android-most-popular-google-play-apps?category={0}&sort=48price=all'.format(category)
        hp = HTMLTableParser()
        data = hp.parse_url(URL)[0][1]
        website_url = requests.get(URL).text
        soup = BeautifulSoup(website_url, 'lxml')
        table = soup.find('table', {'class':'table'})

        httrs = []
        for a in table.find_all('td', {'style':'text-align:left;'}):
            a = a.find('a')
            httrs.append(a.attrs['href'])
        app_urls = []
        for text in httrs:
            extracted = text.rsplit('/',2)[-1]
            app_urls.append(extracted)

        data['app_id'] = app_urls
        data['category'] = category

        logging.warning('Data for {} was stored'.format(category))
        return data.to_csv('var/data/{0}.csv'.format(category))

    except:
       logging.warning('Something went wrong when saving data.') 

def create_list_of_app_ids():
    path = r'var/data'
    files = glob.glob(path + '/*.csv')
    files_list = []

    for filename in files:
        df = pd.read_csv(filename, index_col=None, header = 0)
        files_list.append(df)

    data = pd.concat(files_list, axis=0, ignore_index=True)
    return data

def fetch_most_relevant_comments(app_id):
    try:
        comments = reviews(
            app_id,
            lang='pt-BR', 
            country='br', 
            sort=Sort.MOST_RELEVANT
        ) 
        if len(comments) > 0:
            df = pd.DataFrame.from_dict(comments)
            out_folder = 'var/data/{0}'.format(app_id)
            if not os.path.exists(out_folder):
                os.mkdir(out_folder)
            df.to_csv(r'var/data/{0}/MOST_RELEVANT.csv'.format(app_id))
            print('Most relevant comments for app: {0} stored.'.format(app_id))
        else:
            print('not found')
    except:
        logging.warning('Something went when saving data for app: {0}.'.format(app_id)) 


def fetch_most_relevants_comments_all_apks(app_id_list):
    for app_id in app_id_list:
        fetch_most_relevant_comments(app_id)
        time.sleep(1.2 + np.random.normal(0,0.2,1))


def read_files_in_folder(app_id):
    path = r'var/data/{0}'.format(app_id)
    files = glob.glob(path + '/*.csv')
    if len(files) > 1:
        files_list = []
        for filename in files:
            df = pd.read_csv(filename, index_col=None, header=0)
            files_list.append(df)
        data = pd.concat(files_list, axis=0, ignore_index=0)
        return data
    elif len(files) == 0:
        data = pd.read_csv(files[0])
        return data
    else:
        return None 

def fetch_and_store_comments(app_id):
    try:
        comments = reviews(
                app_id,	
                lang='pt-BR', 
                country='br', 
                sort=Sort.NEWEST, 
                count=100, 
                )

        # Read dataframes and compare them
        df_comments = pd.DataFrame.from_dict(comments)
        try:
            df_folder = read_files_in_folder(app_id)
            df_comparison = pd.concat([df_comments, df_folder])
            df_comparison['at'] = pd.to_datetime(df_comparison['at'])
            since_comments = df_comments['at'].min()
            #since_comparison = df_comparison['at'].min()
            until_comparison = df_comparison['at'].max()
            df_comparison = df_comparison.drop_duplicates(['at', 'userName', 'content'])
            df = df_comparison[(df_comparison['at'] > since_comments) & (df_comparison['at'] < until_comparison)]
            # Store data
            df.to_csv(r'var/data/{0}/{1}_{2}.csv'.format(app_id, since_comments.strftime('%Y-%m-%d'), until_comparison.strftime('%Y-%m-%d')))
        except:
            df_comments['at'] = pd.to_datetime(df_comments['at'])
            since_comments = df_comments['at'].min()
            until_comments = df_comments['at'].max()
            out_folder = 'var/data/{0}'.format(app_id)
            if not os.path.exists(out_folder):
                os.mkdir(out_folder)
            full_path = os.path.join(out_folder, '{0}_{1}.csv'.format(since_comments.strftime('%Y-%m-%d'), until_comments.strftime('%Y-%m-%d')))
            df_comments.to_csv(full_path)
    except:
        print('ERROR saving data from app id: {0}'.format(app_id))


def fetch_and_store_comments_all_apks(app_id_list):
        for app_id in app_id_list:
            try:
                fetch_and_store_comments(app_id)
                time.sleep(1.2 + np.random.normal(0,0.2,1))
                logging.info(r'Data for app {0} were stored successfully'.format(app_id))
            except:
                logging.warning(r'Could not store data for app {}. Action needed: Inspect.'.format(app_id))
