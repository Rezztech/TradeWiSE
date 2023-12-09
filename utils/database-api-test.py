#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#

import requests

# Endpoint URL
url = 'http://database-api/balance_sheet/'

# Test data for posting a balance sheet
post_data = {
    "ticker_symbol": "TEST",
    "reporting_year": 2020,
    "reporting_season": 4,
    "cash": 100000,
}

# Sending a POST request
response = requests.post(url, json=post_data)
print("POST Response:", response.json())

# Test data for getting a balance sheet
get_url = f'{url}TEST/2020/4'

# Sending a GET request
response = requests.get(get_url)
print("GET Response:", response.json())

# Deleting the balance sheet
response = requests.delete(get_url)
print("DELETE Response:", response.json())
