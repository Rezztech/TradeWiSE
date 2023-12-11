#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# TradeWiSE Project
#
# This file is part of the TradeWiSE project, an automated trading and financial analysis platform.
# It is licensed under the Mozilla Public License 2.0 (MPL 2.0), which allows for wide use and modification
# while ensuring that enhancements and modifications remain available to the community.
#
# You can find the MPL 2.0 license in the root directory of the project or at https://www.mozilla.org/MPL/2.0/.
#
# Copyright (c) 2023 by wildfootw <wildfootw@wildfoo.tw>
#

import requests
import pandas as pd
from io import StringIO
import logging
from datetime import datetime
import threading
import queue
import time

# URLs for different types of financial reports
REPORT_URLS = {
    "balance_sheet": "https://mops.twse.com.tw/mops/web/ajax_t164sb03",
    "income_statement": "https://mops.twse.com.tw/mops/web/ajax_t164sb04",
    "cash_flow": "https://mops.twse.com.tw/mops/web/ajax_t164sb05"
}

# Set up logging
logging.basicConfig(level=logging.INFO)

# Task Queue
task_queue = queue.Queue()

# Rate Limiter
REQUEST_INTERVAL = 1  # in seconds

# Function to extract report data
def extract_report_data(html_dataframe, year, season, report_type):
    # Season to date mapping
    season_to_date = {1: "03月31日", 2: "06月30日", 3: "09月30日", 4: "12月31日"}
    date_col = f"{year}年{season_to_date[season]}"

    # Construct column names based on year and season
    year_season_col = f"民國{year}年第{season}季"

    # Change column name according to DataFrame structure
    key_col_name = html_dataframe[year_season_col]["單位：新台幣仟元"]["會計項目"].columns[0]

    # Selecting the key and value columns
    keys = html_dataframe[year_season_col]["單位：新台幣仟元"]["會計項目"][key_col_name]
    values = html_dataframe[year_season_col]["單位：新台幣仟元"][date_col]["金額"]

    # Creating a dictionary from the selected columns
    data_dict = dict(zip(keys, values))
    return data_dict

# Function to crawl financial report
def crawl_financial_report(url, ticker_symbol, year, season):
    form_data = {
        'encodeURIComponent': 1,
        'step': 1,
        'firstin': 1,
        'off': 1,
        'co_id': stock_number,
        'year': year,
        'season': season,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    with requests.Session() as s:
        r = s.post(url, data=form_data, headers=headers)
        if r.status_code != 200:
            print(f"Failed to retrieve data: Status code {r.status_code}")
            return None
        try:
            # Convert the HTML string to a file-like object
            html_string = StringIO(r.text)
            html_dataframe = pandas.read_html(html_string)[1].fillna("")
            return html_dataframe

        except Exception as e:
            print(f"Error occurred while parsing HTML: {e}")
            return None

# Worker function for handling tasks
def worker():
    while True:
        task = task_queue.get()
        try:
            process_task(task)
            time.sleep(REQUEST_INTERVAL)  # Rate limiting
        except Exception as e:
            logging.error(f"Error processing task: {e}")
        finally:
            task_queue.task_done()

# Function to process each task
def process_task(task):
    ticker_symbol, year, season, report_type = task
    url = REPORT_URLS[report_type]
    html_dataframe = crawl_financial_report(url, ticker_symbol, year, season)
    if html_dataframe is not None:
        data_dict = extract_report_data(html_dataframe, year, season, report_type)
        logging.info(f"Processed {report_type} for ticker {ticker_symbol}, year {year}, season {season}")
        # Further processing and storing data
        store_data(data_dict)

# Function to store data into database
def store_data(data):
    # Store data into database through internal API
    pass

# Initialize and start worker threads
NUM_WORKERS = 5
for _ in range(NUM_WORKERS):
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

# Function to schedule crawling tasks
def schedule_crawling_tasks():
    current_year = datetime.now().year
    report_types = ["balance_sheet", "income_statement", "cash_flow"]
    for ticker_symbol in all_ticker_symbols:  # List of all ticker symbols
        for report_type in report_types:
            for year in range(current_year, 1999, -1):  # Historical data from current year to 2000
                for season in range(1, 5):
                    task_queue.put((ticker_symbol, year, season, report_type))

# Function to fetch new data periodically
def fetch_new_data():
    # Periodically add new tasks to the queue for the latest data
    pass

# Function to start the crawler
def start_crawler():
    schedule_crawling_tasks()
    fetch_new_data()
    task_queue.join()

# Example call to start the crawler
start_crawler()

