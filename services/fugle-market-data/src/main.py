from fastapi import FastAPI
from fugle_marketdata import RestClient
import os

fugle_marketdata_api_key = os.getenv('FUGLE_MARKET_DATA_API_KEY')

app = FastAPI()

def get_stock_price(symbol: str):
    client = RestClient(api_key=fugle_marketdata_api_key)
    data = client.stock.intraday.quote(symbol=symbol)
    # Extracting specific data from the response
    price_data = {
        "symbol": symbol,
        "name":          data['name'],
        "lastPrice":     data['lastPrice'],
        "openPrice":     data['openPrice'],
        "highPrice":     data['highPrice'],
        "lowPrice":      data['lowPrice'],
        "closePrice":    data['closePrice'],
        "change":        data['change'],
        "changePercent": data['changePercent']
    }
    return price_data

@app.get("/price/{symbol}")
async def read_price(symbol: str):
    return get_stock_price(symbol)
