from flask import render_template, request
from repositories import quotes_repository

def getQuotesPage(quotes = []):
  return render_template('pages/quotes.html', quotes=quotes)


def getQuotes():
  symbol = request.form['symbol']
  quotes = quotes_repository.getStockQuotes(symbol)
  return getQuotesPage(quotes)