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

from fastapi import FastAPI, HTTPException, status
from pymongo import MongoClient
from utils.encoder import JSONEncoder
from pydantic import BaseModel
import json
import os

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

# API logic
@app.get("/")
def read_root():
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
