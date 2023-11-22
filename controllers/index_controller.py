from flask import render_template

def getIndexPage():
  return render_template('pages/index.html')