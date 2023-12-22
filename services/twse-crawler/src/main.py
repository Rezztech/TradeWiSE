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
import logging
import functools
import time
import os
from io import StringIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Set up logging
log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(message)s")

class RateLimiter:
    def __init__(self, calls_per_second):
        self.period = 1.0 / calls_per_second
        self.last_called = time.monotonic()

    def wait(self):
        current = time.monotonic()
        sleep_for = self.last_called + self.period - current
        if sleep_for > 0:
            logging.debug(f"Rate limiter active, sleeping for {sleep_for} seconds")
            time.sleep(sleep_for)
        self.last_called = time.monotonic()
        logging.debug("Rate limiter lock released")

def rate_limited(func):
    # Use functools.wraps to preserve metadata of the original function
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        limiter.wait()
        # Call the original function and return its result
        return func(*args, **kwargs)
    return wrapped

limiter = RateLimiter(calls_per_second=1)
app = FastAPI()

@rate_limited
def crawl_financial_report(ticker_symbol, year, season, report_type):
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
    try:
        response = requests.post(url, data=form_data, headers=headers)
        logging.debug(f"Received response for {url}, status: {response.status_code}")
        if response.status_code != 200:
            logging.warning(f"Failed to retrieve data: Status code {response.status_code}")
            return {"status_code": response.status_code, "message": "Failed to retrieve data"}

        if "查無所需資料！" in response.text:
            logging.info("No data found for the given parameters.")
            return {"status_code": 404, "message": "No Data Found"}

        return {"status_code": 200, "data": response.text}

    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return {"status_code": 500, "message": "Internal Server Error"}

def sanitize_balance_sheet(response_text, year, season):
    try:
        html_dataframe = pandas.read_html(StringIO(response_text))[1].fillna("")

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
        return {"status_code": 200, "data": data_dict}

    except ValueError as e:
        logging.error(f"Data parsing error with pandas: {e}")
        return {"status_code": 500, "message": "Error parsing HTML data"}
    except KeyError as e:
        logging.error(f"Key error in data extraction, possible incorrect DataFrame indexing: {e}")
        return {"status_code": 500, "message": "Key error in data extraction"}
    except Exception as e:
        logging.error(f"Unexpected error in data extraction: {e}")
        return {"status_code": 500, "message": "Unknown error occurred in data extraction"}

# Store data into database
def store_data(ticker_symbol, year, season, report_type, data):
    # Base URL for the database API
    base_url = 'http://database-api/'

    # Define the URL based on report_type
    if report_type == "balance_sheet":
        url = f'{base_url}balance_sheet/'
    elif report_type == "income_statement":
        url = f'{base_url}income_statement/'
    elif report_type == "cash_flow":
        url = f'{base_url}cash_flow/'
    else:
        logging.error(f"Invalid report type: {report_type}")
        return {"status_code": 400, "message": "Invalid report type"}

    # Construct the POST data
    post_data = {
        "ticker_symbol": ticker_symbol,
        "reporting_year": year,
        "reporting_season": season,
    }
    post_data.update(data)  # Add the financial report data

    try:
        response = requests.post(url, json=post_data)

        if response.status_code == 200:
            logging.info("Data successfully stored in database")
            return {"status_code": 200, "message": "Data stored successfully"}
        else:
            logging.error(f"Failed to store data in database. Status code: {response.status_code}, Response: {response.text}")
            return {"status_code": response.status_code, "message": "Failed to store data in database"}

    except requests.RequestException as e:
        logging.error(f"Request error when storing data: {e}")
        return {"status_code": 500, "message": "Internal Server Error"}

# Function to process each report
def process_report(ticker_symbol, year, season, report_type):
    logging.info(f"Processing report for ticker {ticker_symbol}, year: {year}, season: {season}, type: {report_type}")

    # Retrieve the financial report data
    report_result = crawl_financial_report(ticker_symbol, year, season, report_type)

    # Check if data is available
    if report_result.get("data"):
        sanitized_report = None
        if report_type == "balance_sheet":
            sanitized_report = sanitize_balance_sheet(report_result["data"], year, season)
        elif report_type == "income_statement":
            # Place logic here for income statement extraction
            pass
        elif report_type == "cash_flow":
            # Place logic here for cash flow extraction
            pass
        logging.info(f"Completed data extraction for {ticker_symbol}, year: {year}, season: {season}")

        if sanitized_report:
            store_data(ticker_symbol, year, season, report_type, sanitized_report)
            return {"status_code": 200, "message": "Data processed and stored successfully"}

    return {"status_code": report_result.get("status_code", 500), "message": report_result.get("message", "Error")}


class ReportRequest(BaseModel):
    ticker_symbol: str
    year: int
    season: int

@app.post("/balance_sheet/")
def get_balance_sheet(request: ReportRequest):
    result = process_report(request.ticker_symbol, request.year, request.season, "balance_sheet")
    return {"status_code": result["status_code"], "message": result["message"]}

@app.post("/income_statement/")
def get_income_statement(request: ReportRequest):
    result = process_report(request.ticker_symbol, request.year, request.season, "income_statement")
    return {"status_code": result["status_code"], "message": result["message"]}

@app.post("/cash_flow/")
def get_cash_flow(request: ReportRequest):
    result = process_report(request.ticker_symbol, request.year, request.season, "cash_flow")
    return {"status_code": result["status_code"], "message": result["message"]}
