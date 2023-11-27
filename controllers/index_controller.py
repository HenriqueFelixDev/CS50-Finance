from flask import render_template, request, session, jsonify
from cuid2 import Cuid
from repositories import transactions_repository, quotes_repository
from entities.transaction import ActionCreateDTO

def getIndexPage():
  actions = transactions_repository.getActiveActions(userId=session['id'])

  if (len(actions) > 0):
    symbols = map(lambda action: action.symbol, actions)
    quotes = quotes_repository.getStockPrices(symbols)

    for action in actions:
      action.price = quotes[action.symbol]['price']

  return render_template('pages/index.html', actions=actions)


def getRealtimeAction(symbol, shares):
  quote = quotes_repository.getStockQuotes(symbol)[0]
  
  if quote is None:
    error = { 'code': 400, 'error': f'symbol {symbol} not exists' }
    return jsonify(error), 400

  return ActionCreateDTO(
    id=Cuid().generate(),
    symbol=quote['symbol'],
    name=quote['companyName'],
    price=quote['iexRealtimePrice'],
    shares=shares,
    userId=session['id'],
  )

def buyAction():
  symbol = request.form['symbol']
  shares = int(request.form['shares'])

  action = getRealtimeAction(symbol, shares)

  newFunds = session['funds'] - action.fundsDiscount

  if newFunds <= 0:
    error = { 'code': 400, 'error': 'insufficient funds'}
    return jsonify(error), 400
  
  transactions_repository.buyAction(action)

  session['funds'] = newFunds

  return jsonify({ 'result': 'ok' }), 200


def sellAction():
  symbol = request.form['symbol']
  shares = int(request.form['shares'])

  # Verifica se o usuário possui ações daquele símbolo (totalShares >= request.form['shares'])
  action = transactions_repository.getActionBySymbol(symbol, session['id'])

  if action is None:
    error = { 'code': 400, 'error': f'you don\'t have {symbol} shares' }
    return jsonify(error), 400
  
  if action.shares < shares:
    error = { 'code': 400, 'error': 'insufficient shares' }
    return jsonify(error), 400
  
  # Obtém o valor das ações do símbolo em tempo real
  action = getRealtimeAction(symbol, shares)

  if action.price == 0:
    error = {
      'code': 400,
      'error': 'Unable to get current share price. Try again later',
    }

    return jsonify(error), 400

  # Cadastra a transação e atualiza o saldo do usuário
  transactions_repository.sellAction(action)
  
  session['funds'] = session['funds'] + action.fundsDiscount

  return jsonify({ 'result': 'ok' }), 200

