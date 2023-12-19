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
import pandas
import logging
import functools
import time
import os
import datetime
from io import StringIO

# Set up logging
log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(message)s")

class RateLimiter:
    def __init__(self, calls_per_second):
        self.period = 1.0 / calls_per_second
        # Create an asyncio lock for synchronizing access in asynchronous context
        self.lock = asyncio.Lock()
        self.last_called = time.monotonic()

    async def wait(self):
        # Acquire the lock to ensure exclusive access to check/update last_called time
        async with self.lock:
            current = time.monotonic()
            sleep_for = self.last_called + self.period - current
            if sleep_for > 0:
                logging.debug(f"Rate limiter active, sleeping for {sleep_for} seconds")
                await asyncio.sleep(sleep_for)
            self.last_called = time.monotonic()
            logging.debug("Rate limiter lock released")

def rate_limited(func):
    # Use functools.wraps to preserve metadata of the original function
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        await limiter.wait()
        # Call the original function and return its result
        return await func(*args, **kwargs)
    return wrapped

# Async function to extract balance sheet
async def extract_balance_sheet(html_dataframe, year, season):
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
@rate_limited
async def crawl_financial_report(ticker_symbol, year, season, report_type):
    # URLs for different types of financial reports
    report_urls = {
        "balance_sheet":    "https://mops.twse.com.tw/mops/web/ajax_t164sb03",
        "income_statement": "https://mops.twse.com.tw/mops/web/ajax_t164sb04",
        "cash_flow":        "https://mops.twse.com.tw/mops/web/ajax_t164sb05"
    }
    url = report_urls[report_type]

    logging.debug(f"Starting request for {url}, ticker: {ticker_symbol}, year: {year}, season: {season}")

    form_data = {
        'encodeURIComponent': 1,
        'step': 1,
        'firstin': 1,
        'off': 1,
        'co_id': ticker_symbol,
        'year': year,
        'season': season,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data, headers=headers) as response:
            logging.debug(f"Received response for {url}, status: {response.status}")
            if response.status != 200:
                logging.warning(f"Failed to retrieve data: Status code {response.status}")
                return {"data": None, "message": "Internal Server Error"}
            try:
                text = await response.text()
                try:
                    html_dataframe = pandas.read_html(StringIO(text))[1].fillna("")
                    return {"data": html_dataframe, "message": "Data successfully retrieved"}
                except ValueError:
                    # Specific handling for no tables found in HTML
                    if "查無所需資料！" in text:
                        logging.info("No data found for the given parameters.")
                        return {"data": None, "message": "No Data Found"}
                    else:
                        logging.warning("HTML parsed but contains no tables.")
                        return {"data": None, "message": "Internal Server Error"}
            except Exception as e:
                # Update this message to reflect other types of parsing errors
                logging.warning(f"Unexpected error occurred during HTML parsing or DataFrame creation: {e}")
                return {"data": None, "message": "Internal Server Error"}

# Async function to store data into database
async def store_data(ticker_symbol, year, season, report_type, data):
    logging.info(data)

# Function to process each report
async def process_report(ticker_symbol, year, season, report_type):
    logging.info(f"Processing report for ticker {ticker_symbol}, year: {year}, season: {season}, type: {report_type}")

    # Retrieve the financial report data
    report_result = await crawl_financial_report(ticker_symbol, year, season, report_type)

    report_result_data = {}
    # Check if data is available
    if report_result["data"] is not None:
        if report_type == "balance_sheet":
            report_result_data = await extract_balance_sheet(report_result["data"], year, season)
        elif report_type == "income_statement":
            # Place logic here for income statement extraction
            pass
        elif report_type == "cash_flow":
            # Place logic here for cash flow extraction
            pass
        logging.info(f"Completed data extraction for {ticker_symbol}, year: {year}, season: {season}")
    else:
        # Log the message if no data was found or an error occurred
        report_result_data["message"] = report_result["message"]
    await store_data(ticker_symbol, year, season, report_type, report_result_data)

async def task_worker():
    while True:
        ticker_symbol, year, season, report_type = await task_queue.get()
        await process_report(ticker_symbol, year, season, report_type)
        task_queue.task_done()

