from flask import render_template, request, session, jsonify
from cuid2 import Cuid
from repositories import transactions_repository, quotes_repository
from entities.transaction import ActionCreateDTO

def getIndexPage():
  actions = transactions_repository.getActiveActions(userId=session['id'])

  symbols = map(lambda action: action.symbol, actions)
  quotes = quotes_repository.getStockPrices(symbols)

  for action in actions:
    action.price = quotes[action.symbol]['price']

  return render_template('pages/index.html', actions=actions)


def buyAction():
  symbol = request.form['symbol']
  shares = int(request.form['shares'])

  quote = quotes_repository.getStockQuotes(symbol)[0]
  
  if quote is None:
    error = { 'code': 400, 'error': f'symbol {symbol} not exists' }
    return jsonify(error), 400

  action = ActionCreateDTO(
    id=Cuid().generate(),
    symbol=quote['symbol'],
    name=quote['companyName'],
    price=quote['iexRealtimePrice'],
    shares=shares,
    userId=session['id'],
  )

  newFunds = session['funds'] - action.fundsDiscount

  if newFunds <= 0:
    error = { 'code': 400, 'error': 'missing funds'}
    return jsonify(error), 400
  
  transactions_repository.buyAction(action)

  session['funds'] = newFunds

  return jsonify({ 'result': 'ok' }), 200



