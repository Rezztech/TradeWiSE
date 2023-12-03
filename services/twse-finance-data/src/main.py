#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyleft (ɔ) 2023 wildfootw <wildfootw@wildfoo.tw>
#
# Distributed under terms of the MIT license.

import requests
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine  # Example for SQLAlchemy

def financial_statement(year, season, report_type='綜合損益彙總表'):
    # ... (existing scraping function)

def store_data_in_database(data):
    # Function to store data in the database
    # This will depend on your database schema and ORM/database driver you are using
    engine = create_engine('your-database-connection-string')
    data.to_sql('financial_statements', engine, if_exists='append')

def scheduled_job():
    print("Fetching financial data...")
    # Example: Fetching data for 2021, season 1
    data = financial_statement(2021, 1)
    store_data_in_database(data)

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', hours=24)  # Adjust the interval as needed
scheduler.start()

# To keep the script running
try:
    import time
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

