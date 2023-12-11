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
import pandas
from io import StringIO
from apscheduler.schedulers.background import BackgroundScheduler

# URLs for different types of financial reports
balance_sheet_url = "https://mops.twse.com.tw/mops/web/ajax_t164sb03"       # URL for Balance Sheet
income_statement_url = "https://mops.twse.com.tw/mops/web/ajax_t164sb04"    # URL for Income Statement
cash_flow_url = "https://mops.twse.com.tw/mops/web/ajax_t164sb05"           # URL for Cash Flow Statement

def extract_balance_sheet(html_dataframe, year, season):
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

def crawl_financial_report(url, stock_number, year, season):
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


# Example usage
stock_number = 2330
year = 111
season = 4
html_dataframe = crawl_financial_report(balance_sheet_url, stock_number, year, season)
data_dict = extract_balance_sheet(html_dataframe, year, season)
print(data_dict)

def store_data_in_database(data):
    engine = create_engine('your-database-connection-string')
    data.to_sql('financial_statements', engine, if_exists='append')

def scheduled_job():
    print("Fetching financial data...")
    # Example: Fetching data for 2021, season 1
    data = financial_statement(2021, 1)
    store_data_in_database(data)

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', hours=24)  # Adjust the interval as needed
scheduler.start()

# To keep the script running
try:
    import time
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

