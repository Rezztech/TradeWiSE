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

from fastapi import FastAPI, HTTPException, Body
from fastapi import Depends
from models import create_tables, SessionLocal
from models import BalanceSheet
from schemas import BalanceSheetSchema
from sqlalchemy.orm import Session
import utils

app = FastAPI()

# Create database tables
create_tables()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API logic
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/balance_sheet/")
async def create_balance_sheet(balance_sheet_schema: BalanceSheetSchema, db: Session = Depends(get_db)):
    # Check if company exists, if not, create a new one
    company = db.query(Company).filter(Company.ticker_symbol == balance_sheet_schema.ticker_symbol).first()
    if not company:
        company = Company(ticker_symbol=balance_sheet_schema.ticker_symbol)
        db.add(company)
        db.commit()
        db.refresh(company)

    # Now create the balance sheet with the company's ID
    balance_sheet = utils.convert_schema_to_db_model(company.id, balance_sheet_schema)
    db.add(balance_sheet)
    db.commit()
    return {"status": "success"}

@app.get("/balance_sheet/{ticker_symbol}/{year}/{season}")
async def get_balance_sheet(ticker_symbol: str, year: int, season: int, db: Session = Depends(get_db)):
    # Logic to fetch balance sheet data from the database
    balance_sheet_data = db.query(BalanceSheet).filter(
        BalanceSheet.ticker_symbol == ticker_symbol,
        BalanceSheet.year == year,
        BalanceSheet.season == season
    ).first()

    if balance_sheet_data is None:
        raise HTTPException(status_code=404, detail="Balance Sheet not found")

    return balance_sheet_data

