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

def determine_start_year_and_season():
    """
    Determines the starting season and year for data collection based on the current date.
    The logic is as follows:
    - Jan to Mar: Collect from the previous year's 4th season.
    - Apr to Jun: Start from the current year's 1st season.
    - Jul to Sep: Start from the current year's 2nd season.
    - Oct to Dec: Start from the current year's 3rd season.

    Returns:
        tuple: A tuple containing the starting year and season.
    """
    now = datetime.datetime.now()
    current_year = now.year - 1911  # Convert to the local calendar year
    current_month = now.month

    # Determine the start season and year based on the current month
    if 1 <= current_month <= 3:
        start_season = 4
        start_year = current_year - 1
    elif 4 <= current_month <= 6:
        start_season = 1
        start_year = current_year
    elif 7 <= current_month <= 9:
        start_season = 2
        start_year = current_year
    else:  # 10 <= current_month <= 12
        start_season = 3
        start_year = current_year

    return start_year, start_season

async def schedule_tasks(all_ticker_symbols, report_types, task_queue):
    """
    Schedules tasks for collecting data based on the starting season and year.
    Iterates over each ticker symbol and report type, scheduling tasks for each
    combination from the starting point going back to the year 110.

    Parameters:
        all_ticker_symbols (list): A list of all ticker symbols to be processed.
        report_types (list): A list of report types to be processed.
        task_queue (asyncio.Queue): An asyncio Queue where tasks will be put for processing.
    """
    start_year, start_season = determine_start_year_and_season()

    for ticker_symbol in all_ticker_symbols:
        for report_type in report_types:
            # Schedule tasks for each ticker symbol and report type combination.
            for year in range(start_year, 82, -1):
                # If it's the start year (the first year in our iteration), we use the calculated start season
                # Otherwise, for all previous years, we start from the 4th season
                season_start = start_season if year == start_year else 4

                # Iterate over the seasons in reverse order (4 to 1) for each year
                for season in range(season_start, 0, -1):
                    logging.debug(f"Scheduled task for report type {report_type}, ticker {ticker_symbol}, year {year}, season {season}")
                    await task_queue.put((ticker_symbol, year, season, report_type))

def retrieve_and_update_reports():
    companies = get_company_list_from_database()
    for company in companies:
        latest_version = get_latest_defined_version_for_company(company)
        for season in get_past_seasons(2):
            current_version = get_version_from_database(company, season)
            if current_version == "NDF":
                continue
            if current_version != latest_version:
                report = trigger_crawler_to_retrieve_report(company, season)
                if report is not None:
                    update_database_with_new_report(company, season, report)
                    update_local_version_table(company, season)

def get_company_list_from_database():
    # Implement database call to get the list of companies
    pass

def get_latest_defined_version_for_company(company):
    # Implement database call to get the latest defined version for company reports
    pass

def get_past_seasons(number_of_seasons):
    # Implement logic to calculate past seasons
    pass

def get_version_from_database(company, season):
    # Implement database call to get the version of the report for the given company and season
    pass

def trigger_crawler_to_retrieve_report(company, season):
    # Implement logic to call the crawler service and retrieve the report
    pass

def update_database_with_new_report(company, season, report):
    # Implement database update logic
    pass

def update_local_version_table(company, season):
    # Implement logic to update local version table with the new version
    pass

def schedule_updates():
    scheduler = BackgroundScheduler()
    scheduler.add_job(retrieve_and_update_reports, 'cron', hour=14, minute=0)
    scheduler.add_job(retrieve_and_update_reports, 'date', run_date=datetime.datetime.now())
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

