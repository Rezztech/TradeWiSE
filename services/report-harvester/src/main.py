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

from apscheduler.schedulers.background import BackgroundScheduler
import requests
import logging
import time
import os
import datetime

# Set up logging
log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(message)s")

# Define your report types
REPORT_TYPES = {
    'balance_sheet': 'REPORT_VERSION_BALANCE_SHEET',
    'income_statement': 'REPORT_VERSION_INCOME_STATEMENT',
    'cash_flow': 'REPORT_VERSION_CASH_FLOW'
}

def update_financial_reports():
    # Retrieve the list of company identifiers
    ticker_symbols = retrieve_ticker_symbols()

    # Iterate over each report type and its corresponding latest version from the environment variable
    for report_type, env_var in REPORT_TYPES.items():
        latest_version = os.getenv(env_var)

        # Update financial reports for each company
        for ticker_symbol in ticker_symbols:
            # Retrieve the current version information of the company's reports
            report_version_table = retrieve_financial_report_version_table(ticker_symbol, report_type)

            # Update the previous season's financial report
            previous_season_tuple = get_past_season(1)
            report_version_table = retrieve_financial_report(ticker_symbol, report_type, previous_season_tuple, report_version_table, latest_version)

            # Continue retrieving and updating data from the preceding seasons until the version is "NDF"
            season_decrement = 2 # Preceding seasons
            while True:
                past_season_tuple = get_past_season(season_decrement)
                # First check to minimize the crawler request if the version is already "NDF"
                if report_version_table.get(past_season_tuple[0]).get(past_season_tuple[1]) == "NDF":
                    break

                report_version_table = retrieve_financial_report(ticker_symbol, report_type, past_season_tuple, report_version_table, latest_version)

                # Second check after attempting to update, in case the crawler finds no new data
                if report_version_table.get(past_season_tuple[0]).get(past_season_tuple[1]) == "NDF":
                    break

                season_decrement += 1

def retrieve_ticker_symbols():
    # [TODO] Implement logic to retrieve the list of companies from the database
    return ["2330", "2331"]

def retrieve_financial_report_version_table(ticker_symbol, report_type):
    # Implement logic to retrieve the company's report version information
    pass

def retrieve_financial_report(ticker_symbol, report_type, season_tuple, version_table, latest_version):
    # Implement logic to retrieve and update the version information for the specified season
    # This should also update the version_info dictionary
    pass

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

    return past_year, past_season

def schedule_updates():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_finance_reports, 'cron', hour=14, minute=0)
    scheduler.add_job(update_finance_reports, 'date', run_date=datetime.datetime.now())
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

