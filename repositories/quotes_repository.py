import urllib.request, urllib.parse
import json
import os

def getStockPrices(symbols: list[str]):
  token = os.getenv('IEX_API_KEY')
  encodedSymbols = urllib.parse.quote_plus(','.join(symbols))
  url = f'https://cloud.iexapis.com/v1/stock/market/batch?&types=price&symbols={encodedSymbols}&token={token}'
  
  response = urllib.request.urlopen(url, timeout=15)
  return json.loads(response.read())


def getStockQuotes(symbol: str):
  token = os.getenv('IEX_API_KEY')
  url = f'https://api.iex.cloud/v1/data/core/quote/{symbol}?token={token}'

  response = urllib.request.urlopen(url, timeout=15)
  return json.loads(response.read())
  