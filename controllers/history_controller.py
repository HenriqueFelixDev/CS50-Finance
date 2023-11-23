from flask import render_template, session
from repositories import transactions_repository

def getHistoryPage():
  transactions = transactions_repository.getAllTransactions(userId=session['id'])
  return render_template('pages/history.html', transactions=transactions)