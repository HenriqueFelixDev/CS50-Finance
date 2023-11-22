from flask import Flask, request, render_template
from flask_session import Session
import core.filters as filters
from controllers import auth_controller

app = Flask(__name__)

# Define jinja custom filters
app.jinja_env.filters['usd'] = filters.usd
app.jinja_env.filters['date'] = filters.date
app.jinja_env.filters['datetime'] = filters.datetime

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)


@app.route('/', methods=['GET'])
def index():
  return render_template('pages/index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    return auth_controller.signUp()
  
  return auth_controller.getSignUpPage()


if __name__ == '__main__':
  app.run()