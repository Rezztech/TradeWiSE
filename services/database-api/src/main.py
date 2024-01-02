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

from typing import Dict
import json
import os
import logging

log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pymongo import MongoClient

from utils.encoder import JSONEncoder


# Pydantic model for balance sheet request validation
class ReportRequest(BaseModel):
    version: str
    ticker_symbol: str
    reporting_year: int
    reporting_season: int

app = FastAPI()

# Load environment variables
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DB = os.getenv("MONGO_DATABASE")

# MongoDB connection
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@database:27017/")
db = client[MONGO_DB]

def get_version_table(ticker_symbol: str, report_type: str) -> Dict:
    collection = db[report_type]

    # Query for all documents related to the specific ticker_symbol
    query_result = collection.find({"ticker_symbol": ticker_symbol})

    # Building the return dictionary
    version_table = {}
    for doc in query_result:
        year = doc.get("reporting_year")
        season = doc.get("reporting_season")
        version = doc.get("version")

        #logging.debug(f"Processing document: Year={year}, Season={season}, Version={version}")
        # Ensure the year key exists in the version table
        if year not in version_table:
            version_table[year] = {}

        # Add season and version information
        version_table[year][season] = version

    return version_table

@app.get("/{ticker_symbol}/{report_type}/version_table")
async def get_version_table_endpoint(ticker_symbol: str, report_type: str):
    try:
        reports = get_version_table(ticker_symbol, report_type)
        return reports
    except Exception as e:
        logging.error(f"Error fetching version table: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.get("/health")
def health_check():
    return {"Hello": "World"}

@app.post("/create_report/{report_type}/")
async def create_report(report_type: str, report_request: ReportRequest):
    collection = db[report_type]  # Use report_type to select the appropriate collection
    existing_report = collection.find_one({
        "ticker_symbol": report_request.ticker_symbol,
        "reporting_year": report_request.reporting_year,
        "reporting_season": report_request.reporting_season
    })

    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{report_type.capitalize()} report already exists"
        )

    report_data = report_request.dict()
    collection.insert_one(report_data)
    return {"message": f"{report_type.capitalize()} report created"}

@app.get("/{ticker_symbol}/{report_type}/{year}/{season}")
async def get_report(ticker_symbol: str, report_type: str, year: int, season: int):
    collection = db[report_type]
    report = collection.find_one({"ticker_symbol": ticker_symbol, "reporting_year": year, "reporting_season": season})
    if report:
        return json.loads(json.dumps(report, cls=JSONEncoder))
    raise HTTPException(status_code=404, detail=f"{report_type.capitalize()} report not found")

@app.delete("/{ticker_symbol}/{report_type}/{year}/{season}")
async def delete_report(ticker_symbol: str, report_type: str, year: int, season: int):
    collection = db[report_type]
    result = collection.delete_one({"ticker_symbol": ticker_symbol, "reporting_year": year, "reporting_season": season})
    if result.deleted_count:
        return {"message": f"{report_type.capitalize()} report deleted"}
    raise HTTPException(status_code=404, detail=f"{report_type.capitalize()} report not found")
