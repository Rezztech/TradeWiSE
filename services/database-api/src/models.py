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

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base # These SQLAlchemy model is for database
from sqlalchemy.orm import sessionmaker

# Database configuration using environment variables
DATABASE_URL = f"mysql+pymysql://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_PASSWORD')}@database/{os.getenv('MARIADB_DATABASE')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ticker_symbol = Column(String(10))

class BalanceSheet(Base):
    __tablename__ = 'balance_sheet'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    reporting_year = Column(Integer)
    reporting_season = Column(Integer)
    # Current Assets
    cash = Column(Integer)
    fin_assets_fvpl_curr = Column(Integer)
    fin_assets_fvoci_curr = Column(Integer)
    fin_assets_amort_curr = Column(Integer)
    hedging_assets_curr = Column(Integer)
    net_receiv = Column(Integer)
    receiv_related_net = Column(Integer)
    receiv_other_related_net = Column(Integer)
    inventory = Column(Integer)
    other_curr_assets = Column(Integer)
    total_curr_assets = Column(Integer)
    # Non-current Assets
    fin_assets_fvpl_noncurr = Column(Integer)
    fin_assets_fvoci_noncurr = Column(Integer)
    fin_assets_amort_noncurr = Column(Integer)
    equity_inv = Column(Integer)
    ppe = Column(Integer)
    rou_assets = Column(Integer)
    intangible = Column(Integer)
    deferred_tax_asset = Column(Integer)
    other_noncurr_assets = Column(Integer)
    total_noncurr_assets = Column(Integer)
    total_assets = Column(Integer)
    # Current Liabilities
    fin_liab_fvpl_curr = Column(Integer)
    hedging_liab_curr = Column(Integer)
    acct_payable = Column(Integer)
    acct_payable_related = Column(Integer)
    other_payables = Column(Integer)
    tax_liab_curr = Column(Integer)
    other_curr_liab = Column(Integer)
    total_curr_liab = Column(Integer)
    # Non-current Liabilities
    bonds_payable = Column(Integer)
    lt_borrow = Column(Integer)
    deferred_tax_liab = Column(Integer)
    lease_liab_noncurr = Column(Integer)
    other_noncurr_liab = Column(Integer)
    total_noncurr_liab = Column(Integer)
    total_liab = Column(Integer)
    # Equity Attributable to Owners of the Parent
    # Share Capital
    ord_share = Column(Integer)
    total_share_cap = Column(Integer)
    # Capital Reserve
    cap_res_premium = Column(Integer)
    cap_res_diff_subsidiaries = Column(Integer)
    cap_res_eq_changes_subs = Column(Integer)
    cap_res_donated = Column(Integer)
    cap_res_eq_method = Column(Integer)
    cap_res_merger = Column(Integer)
    cap_res_restricted_shares = Column(Integer)
    total_cap_res = Column(Integer)
    # Retained Earnings
    legal_res = Column(Integer)
    special_res = Column(Integer)
    unapp_retained_earn = Column(Integer)
    total_retained_earn = Column(Integer)
    # Other Equity
    total_other_eq = Column(Integer)
    treasury_shares = Column(Integer)
    total_eq_parent = Column(Integer)
    non_ctrl_interests = Column(Integer)
    total_eq = Column(Integer)
    total_liab_eq = Column(Integer)
    anticipate_stock_issue = Column(Integer)
    treasury_shares_held = Column(Integer)

#class IncomeStatement(Base):
#    __tablename__ = 'income_statement'
#    # Define columns
#
#class CashFlowStatement(Base):
#    __tablename__ = 'cash_flow_statement'
#    # Define columns
#
#class MonthlyRevenue(Base):
#    __tablename__ = 'monthly_revenue'
#    # Define columns

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

