from flask import render_template, session
from repositories import transactions_repository, quotes_repository

def getIndexPage():
  actions = transactions_repository.getActiveActions(userId=session['id'])

  symbols = map(lambda action: action.symbol, actions)
  quotes = quotes_repository.getStockPrices(symbols)

  for action in actions:
    action.price = quotes[action.symbol]['price']

  return render_template('pages/index.html', actions=actions)