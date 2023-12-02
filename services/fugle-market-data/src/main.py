from fugle_marketdata import RestClient
import os

fugle_marketdata_api_key = os.getenv('FUGLE_MARKET_DATA_API_KEY')

def get_intraday_quote(symbol):
    client = RestClient(api_key=fugle_marketdata_api_key)
    data = client.stock.intraday.quote(symbol=symbol)
    return data

if __name__ == "__main__":
    # Example usage
    symbol = "2330"  # Replace with desired stock symbol
    quote_data = get_intraday_quote(symbol)
    print(quote_data)

