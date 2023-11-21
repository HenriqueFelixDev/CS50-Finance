from flask import Flask, render_template
import core.filters as filters

app = Flask(__name__)

app.jinja_env.filters['usd'] = filters.usd
app.jinja_env.filters['date'] = filters.date
app.jinja_env.filters['datetime'] = filters.datetime

@app.route('/signup', methods=['GET'])
def index():
  return render_template('pages/signup.html')

if __name__ == '__main__':
  app.run()