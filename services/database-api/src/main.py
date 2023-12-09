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

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from utils.encoder import JSONEncoder
import json
import os

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

@app.post("/balance_sheet/")
async def create_balance_sheet(balance_sheet: dict):
    collection = db.balance_sheets
    collection.insert_one(balance_sheet)
    return {"status": "success"}

@app.get("/balance_sheet/{ticker_symbol}/{year}/{season}")
async def get_balance_sheet(ticker_symbol: str, year: int, season: int):
    collection = db.balance_sheets
    balance_sheet = collection.find_one({"ticker_symbol": ticker_symbol, "reporting_year": year, "reporting_season": season})
    if balance_sheet:
        # Serialize MongoDB document using the custom JSON Encoder
        return json.loads(json.dumps(balance_sheet, cls=JSONEncoder))
    raise HTTPException(status_code=404, detail="Balance sheet not found")

@app.delete("/balance_sheet/{ticker_symbol}/{year}/{season}")
async def delete_balance_sheet(ticker_symbol: str, year: int, season: int):
    collection = db.balance_sheets
    result = collection.delete_one({"ticker_symbol": ticker_symbol, "reporting_year": year, "reporting_season": season})
    if result.deleted_count:
        return {"status": "success", "message": "Balance sheet deleted"}
    raise HTTPException(status_code=404, detail="Balance sheet not found")

