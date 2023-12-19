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

import logging
import os
import datetime
import pika

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

# Function to schedule crawling tasks
async def main():
    global limiter, task_queue
    limiter = RateLimiter(calls_per_second=0.1) # Global instance of RateLimiter
    task_queue = asyncio.Queue() # Global instance of asyncio.Queue

    logging.info("Scheduling crawling tasks")
    #report_types = ["balance_sheet", "income_statement", "cash_flow"]
    report_types = ["balance_sheet"]
    #all_ticker_symbols = ["2330", "2317", "2454", "3008", "1301", "1303", "1326", "2308"]
    all_ticker_symbols = ["2330", "2317"]
    await schedule_tasks(all_ticker_symbols, report_types, task_queue)

    workers = [asyncio.create_task(task_worker()) for _ in range(5)] # Create 5 workers
    # Wait until all tasks are processed
    await task_queue.join()
    # Cancel all workers
    for worker in workers:
        worker.cancel()
    await asyncio.gather(*workers, return_exceptions=True)

# Run the main function
asyncio.run(main())

