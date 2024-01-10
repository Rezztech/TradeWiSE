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

import functools
import logging
import os
import time
from io import StringIO

import pandas
import requests
from fastapi import FastAPI, HTTPException
from lxml import etree
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

limiter = RateLimiter(calls_per_second=10)
app = FastAPI()

@rate_limited
def crawl_financial_report(ticker_symbol, report_type, year, season):
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

        return {"status_code": 200, "data": response.text}

    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return {"status_code": 500, "message": "Internal Server Error"}

# Listed companies, OTC (Over-the-Counter) companies, and emerging stock companies have started to adopt IFRSs (International Financial Reporting Standards) for financial statement preparation since 2013.
def sanitize_balance_sheet_ifrs(year, season, response_text):
    if "查無所需資料！" in response_text:
        logging.info("No data found for the given parameters.")
        return {"status_code": 200, "data": {"version": "NDF"}}

    if "Too many query requests from your ip" in response_text:
        logging.info("Request frequency exceeded the allowed limit.")
        return {"status_code": 429, "message": "Request frequency exceeded the allowed limit"}

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

# Function to generate the POST data
def generate_post_data(ticker_symbol, year, season, data):
    # Construct the POST data
    post_data = {
        "ticker_symbol": ticker_symbol,
        "reporting_year": year,
        "reporting_season": season,
    }
    post_data.update(data)  # Add the financial report data
    if "version" not in post_data:
        post_data["version"] = "v1"
    return post_data

def sanitize_report(report_type, year, season, response_text):
    if report_type == "balance_sheet":
        return sanitize_balance_sheet_ifrs(year, season, response_text)
    elif report_type == "income_statement":
        # return sanitize_income_statement(response_text, year, season)
        pass
    elif report_type == "cash_flow":
        # return sanitize_cash_flow(response_text, year, season)
        pass

# Function to process each report
def process_report(ticker_symbol, report_type, year, season):
    logging.info(f"Processing report for ticker {ticker_symbol}, year: {year}, season: {season}, type: {report_type}")

    # Retrieve the financial report data
    report_result = crawl_financial_report(ticker_symbol, report_type, year, season)
    if report_result.get("status_code") != 200:
        return report_result  # This will contain the status_code and message from crawl_financial_report

    sanitized_report = sanitize_report(report_type, year, season, report_result["data"])
    if sanitized_report.get("status_code") != 200:
        return sanitized_report  # This will contain the status_code and message from sanitize_report

    # Generate POST data with the sanitized report data
    post_data = generate_post_data(ticker_symbol, year, season, sanitized_report["data"])

    logging.info(f"Completed data extraction for {ticker_symbol}, year: {year}, season: {season}")
    return {"status_code": 200, "message": "Success", "data": post_data}

@app.get("/health")
def health_check():
    return {"Hello": "World"}

@app.get("/{ticker_symbol}/{report_type}/{year}/{season}")
def get_financial_report(report_type: str, ticker_symbol: str, year: int, season: int):
    # Ensure that report_type is one of the expected types
    if report_type not in ["balance_sheet", "income_statement", "cash_flow"]:
        raise HTTPException(status_code=400, detail="Invalid report type specified")

    # Call the process_report function with the path parameters
    result = process_report(ticker_symbol, report_type, year, season)

    # If process_report returned an error status code, raise an HTTPException
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])

    # If everything went well, return the sanitized data
    return result["data"]

@app.get('/get_all_companies')
def download_company_info():
    base_url = 'https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y'
    try:
        response = requests.get(base_url)
        response.raise_for_status()

    except Exception as err:
        logging.error(f"HTTP error occurred while crawling: {err}")
        raise

    listed_companies_data = response.text
    root = etree.HTML(listed_companies_data)

    symbol_column_locator = '//tr//*[normalize-space()=\'{}\']/preceding-sibling::*'.format('有價證券代號')
    symbol_column_index = len(root.xpath(symbol_column_locator)) + 1
    name_column_locator = '//tr//*[normalize-space()=\'{}\']/preceding-sibling::*'.format('有價證券名稱')
    name_column_index = len(root.xpath(name_column_locator)) + 1
    row_locator = '//tr[position()>1]'
    rows = root.xpath(row_locator)

    results = []
    for row in rows:
        symbol = row.xpath('.//td[{}]'.format(symbol_column_index))[0].text
        company = row.xpath('.//td[{}]'.format(name_column_index))[0].text
        symbol_company = {
            'symbol': symbol,
            'company': company
        }
        results.append(symbol_company)
    return results
