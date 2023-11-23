from flask import render_template

def getQuotesPage():
  return render_template('pages/quotes.html')