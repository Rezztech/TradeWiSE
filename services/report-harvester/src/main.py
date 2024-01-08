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

import datetime
import logging
import os
import time

import pytz
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import HTTPError

# Set up logging
log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(message)s")

def get_past_season(seasons_back):
    """
    Calculates the year and season going back from the current date based on the number of seasons specified.
    The seasons are based on the financial reporting seasons as follows:
    - Q1: Jan 1 to Mar 31
    - Q2: Apr 1 to Jun 30
    - Q3: Jul 1 to Sep 30
    - Q4: Oct 1 to Dec 31

    Args:                                                                                 seasons_back (int): The number of seasons to go back from the current season.

    Returns:
    tuple: A tuple containing the year and season that is the specified number of seasons back.
    """
    now = datetime.datetime.now()
    current_year = now.year - 1911  # Convert to the local calendar year
    current_month = now.month

    # Determine the current season based on the current month
    if 1 <= current_month <= 3:
        current_season = 1
    elif 4 <= current_month <= 6:
        current_season = 2
    elif 7 <= current_month <= 9:
        current_season = 3
    else:  # 10 <= current_month <= 12
        current_season = 4

    # Calculate the year and season going back the specified number of seasons
    past_year = current_year - (seasons_back // 4)
    past_season = current_season - (seasons_back % 4)
    if past_season <= 0:
        past_season = past_season + 4
        past_year -= 1

    if past_year <= 0:
        raise ValueError("Error: The calculated year is less than or equal to 0.")

    return str(past_year), str(past_season)

def store_financial_report(report_type, post_data):
    # Base URL for the database API
    base_url = 'http://database-api/create_report/'

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

def retrieve_ticker_symbols():
    companies = get_companies_by_crawler()
    synchronize_company(companies)
    symbols = [company['symbol'] for company in companies]
    return symbols

def get_companies_by_crawler() -> list:
    base_url = 'http://mops-crawler'
    url = f'{base_url}/get_all_companies'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred while retrieving report version table: {http_err}")
        raise
    except Exception as err:
        logging.error(f"Error occurred while retrieving report version table: {err}")
        raise

def synchronize_company(companies: list):
    base_url = 'http://database-api'
    url = f'{base_url}/synchronize_company_table'

    try:
        response = requests.post(url, json=companies)
        response.raise_for_status()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred while synchronizing company table: {http_err}")
        raise
    except Exception as err:
        logging.error(f"Error occurred while synchronizing company  table: {err}")
        raise

def retrieve_financial_report_version_table(ticker_symbol, report_type):
    base_url = "http://database-api"
    url = f"{base_url}/{ticker_symbol}/{report_type}/version_table"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Assuming the API returns a JSON response
        version_table = response.json()
        return version_table

    # Handle HTTP errors (e.g., response code 4XX or 5XX)
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred while retrieving report version table: {http_err}")
        raise
    # Handle other errors
    except Exception as err:
        logging.error(f"Error occurred while retrieving report version table: {err}")
        raise

def retrieve_financial_report(ticker_symbol, report_type, year, season):
    base_url = "http://mops-crawler"

    # Construct the full URL with path parameters
    url = f"{base_url}/{ticker_symbol}/{report_type}/{year}/{season}"

    try:
        # Make the GET request to the financial reports API
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()

        # Assuming the API returns a JSON response, parse it
        report_data = response.json()
        return report_data

    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        # You can return a detailed error message here, or re-raise the exception
        # depending on how you want to handle failures.
        # return {"error": str(http_err)}
        raise
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        # You can return a detailed error message here, or re-raise the exception
        # depending on how you want to handle failures.
        # return {"error": str(err)}
        raise

def update_financial_reports():
    """
    Updates financial reports for all companies.

    This function iterates through each company and updates their financial reports (balance sheet, income statement, cash flow) based on the supported version number specified in environment variables. It retrieves the current version of each company's report, compares it against the supported version, and if the version is outdated or missing (indicated by 'NDF'), it will attempt to fetch and store the updated report. The process checks the previous season first and then continues backwards for preceding seasons.
    """
    logging.debug("Starting to update financial reports.")

    # Retrieve the list of company identifiers
    ticker_symbols = retrieve_ticker_symbols()
    logging.debug(f"Retrieved ticker symbols: {ticker_symbols}")

    # Update financial reports for each company
    for ticker_symbol in ticker_symbols:
        logging.debug(f"Updating reports for ticker symbol: {ticker_symbol}")

        # Iterate over each report type and its corresponding supported version
        REPORT_TYPES = {
            'balance_sheet': 'v1',
#            'income_statement': 'v1',
#            'cash_flow': 'v1'
        }

        for report_type, supported_version in REPORT_TYPES.items():
            logging.debug(f"Supported version for {report_type}: {supported_version}")

            # Retrieve the current version information of the company's reports
            report_version_table = retrieve_financial_report_version_table(ticker_symbol, report_type)
            logging.debug(f"Current version table for {ticker_symbol}: {report_version_table}")

            # Update the previous season's financial report
            # Get the version for the past_year and past_season, default to None if not found
            past_year, past_season = get_past_season(1) # Previous season
            past_version = report_version_table.get(past_year, {}).get(past_season, None)
            logging.debug(f"Version for {ticker_symbol} {report_type} {past_year} {past_season}: {past_version}")

            if past_version != supported_version:
                logging.debug(f"Version mismatch for {ticker_symbol} {report_type} {past_year} {past_season}")
                retrieve_result = retrieve_financial_report(ticker_symbol, report_type, past_year, past_season)
                if retrieve_result["version"] == supported_version:
                    store_result = store_financial_report(report_type, retrieve_result)
                    logging.debug(f"Stored financial report for {ticker_symbol} {report_type} {past_year} {past_season}")
                elif retrieve_result["version"] == "NDF":
                    logging.info("No data found for %s %s %s %s", ticker_symbol, report_type, past_year, past_season)

            # Continue retrieving and updating data from the preceding seasons until the version is "NDF"
            season_decrement = 2 # Preceding seasons
            while True:
                past_year, past_season = get_past_season(season_decrement)
                season_decrement += 1
                past_version = report_version_table.get(past_year, {}).get(past_season, None)
                logging.debug(f"Version for {ticker_symbol} {report_type} {past_year} {past_season}: {past_version}")

                # ROC GAAP not supported
                if past_year == "101":
                    logging.info(f"ROC GAAP not supported")
                    break

                # First check to minimize the crawler request if the version is already "NDF"
                if past_version == "NDF":
                    logging.debug(f"No further data to update for {ticker_symbol} {report_type} before {past_year} {past_season}")
                    break

                if past_version == supported_version:
                    logging.debug(f"Supported version already present for {ticker_symbol} {report_type} {past_year} {past_season}")
                    continue

                retrieve_result = retrieve_financial_report(ticker_symbol, report_type, past_year, past_season)
                if retrieve_result["version"] == supported_version:
                    store_result = store_financial_report(report_type, retrieve_result)
                    logging.debug(f"Stored financial report for {ticker_symbol} {report_type} {past_year} {past_season}")

                # Second check after attempting to update, in case the crawler finds no new data
                elif retrieve_result["version"] == "NDF":
                    store_result = store_financial_report(report_type, retrieve_result)
                    logging.info("No data found for %s %s %s %s", ticker_symbol, report_type, past_year, past_season)
                    break

    logging.debug("Finished updating financial reports.")


def schedule_updates():
    scheduler = BackgroundScheduler()
    timezone = pytz.timezone('Asia/Taipei')
    scheduler.add_job(update_financial_reports, 'cron', hour=14, timezone=timezone)
    scheduler.add_job(update_financial_reports, 'date', run_date=datetime.datetime.now())
    scheduler.start()

    # Keep the script running
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    schedule_updates()
