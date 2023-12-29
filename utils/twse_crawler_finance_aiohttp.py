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

import asyncio
import logging
import os
from io import StringIO

import aiohttp
import pandas

# Set up logging
log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(message)s")

# function to extract balance sheet
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

# function to crawl financial report
async def crawl_financial_report(ticker_symbol, year, season, report_type):
    # URLs for different types of financial reports
    report_urls = {
        "balance_sheet":    "https://mops.twse.com.tw/mops/web/ajax_t164sb03",
        "income_statement": "https://mops.twse.com.tw/mops/web/ajax_t164sb04",
        "cash_flow":        "https://mops.twse.com.tw/mops/web/ajax_t164sb05"
    }
    url = report_urls[report_type]

    logging.debug(f"Starting request for {url}, ticker: {ticker_symbol}, year: {year}, season: {season}")

    form_data = { 'encodeURIComponent': 1, 'step': 1, 'firstin': 1, 'off': 1, 'co_id': ticker_symbol, 'year': year, 'season': season, }
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0' }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data, headers=headers) as response:
            logging.debug(f"Received response for {url}, status: {response.status}")
            if response.status != 200:
                logging.error(f"Failed to retrieve data: Status code {response.status}")
                return None
            try:
                text = await response.text()
                html_dataframe = pandas.read_html(StringIO(text))[1].fillna("")
                return html_dataframe
            except Exception as e:
                logging.error(f"Error occurred while parsing HTML: {e}")
                return None

async def main():
    ticker_symbol = "2330"
    year = 111
    season = 4
    report_type = "balance_sheet"
    logging.debug(f"Processing report for ticker {ticker_symbol}, year: {year}, season: {season}, type: {report_type}")
    html_dataframe = await crawl_financial_report(ticker_symbol, year, season, report_type)
    if html_dataframe is not None:
        extracted_data = {}
        if report_type == "balance_sheet":
            extracted_data = await extract_balance_sheet(html_dataframe, year, season)
        elif report_type == "income_statement":
            pass
        elif report_type == "cash_flow":
            pass
        logging.debug(f"Completed data extraction for {ticker_symbol}, year: {year}, season: {season}")
        print(extracted_data)

if __name__ == "__main__":
    asyncio.run(main())
