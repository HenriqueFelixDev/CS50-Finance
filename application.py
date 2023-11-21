from flask import Flask
import core.filters as filters

app = Flask(__name__)

app.jinja_env.filters['usd'] = filters.usd
app.jinja_env.filters['date'] = filters.date
app.jinja_env.filters['datetime'] = filters.datetime

@app.route('/')
def index():
  return 'OK'

if __name__ == '__main__':
  app.run()