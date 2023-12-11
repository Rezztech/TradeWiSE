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

import aiohttp
import asyncio
import pandas as pd
from io import StringIO
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import functools
import time

# URLs for different types of financial reports
REPORT_URLS = {
    "balance_sheet": "https://mops.twse.com.tw/mops/web/ajax_t164sb03",
    "income_statement": "https://mops.twse.com.tw/mops/web/ajax_t164sb04",
    "cash_flow": "https://mops.twse.com.tw/mops/web/ajax_t164sb05"
}

# Set up logging
logging.basicConfig(level=logging.INFO)

class RateLimiter:
    def __init__(self, calls_per_second):
        self.period = 1.0 / calls_per_second
        self.last_called = time.monotonic()

    async def __aenter__(self):
        current = time.monotonic()
        sleep_for = self.last_called + self.period - current
        if sleep_for > 0:
            await asyncio.sleep(sleep_for)
        self.last_called = time.monotonic()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

def rate_limited(calls_per_second):
    limiter = RateLimiter(calls_per_second)

    def decorator(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            async with limiter:
                return await func(*args, **kwargs)
        return wrapped
    return decorator

# Async function to extract report data
async def extract_report_data(html_dataframe, year, season, report_type):
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

# Async function to crawl financial report
@rate_limited(1)  # 1 request per second
async def crawl_financial_report(url, ticker_symbol, year, season):
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
        'User-Agent': 'Your User Agent'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data, headers=headers) as response:
            if response.status != 200:
                logging.error(f"Failed to retrieve data: Status code {response.status}")
                return None
            try:
                text = await response.text()
                html_dataframe = pd.read_html(StringIO(text))[1].fillna("")
                return html_dataframe
            except Exception as e:
                logging.error(f"Error occurred while parsing HTML: {e}")
                return None

# Function to schedule crawling tasks
def schedule_crawling_tasks(scheduler):
    report_types = ["balance_sheet", "income_statement", "cash_flow"]
    current_year = datetime.now().year
    for ticker_symbol in all_ticker_symbols:  # List of all ticker symbols
        for report_type in report_types:
            for year in range(current_year, 1999, -1):  # Historical data
                for season in range(1, 5):
                    scheduler.add_job(
                        crawl_financial_report, 
                        args=(REPORT_URLS[report_type], ticker_symbol, year, season)
                    )

# Main function to start the crawler
async def main():
    scheduler = AsyncIOScheduler()
    schedule_crawling_tasks(scheduler)
    scheduler.start()

    # Keep the script running
    while True:
        await asyncio.sleep(60)

# Run the crawler
asyncio.run(main())

