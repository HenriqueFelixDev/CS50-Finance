from flask import Flask, request, render_template
from flask_session import Session
from core import filters, decorators
from controllers import auth_controller, index_controller

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
@decorators.login_required
def index():
  return index_controller.getIndexPage()


@app.route('/sign-up', methods=['GET', 'POST'])
@decorators.unprotected_route
def signup():
  if request.method == 'POST':
    return auth_controller.signUp()
  
  return auth_controller.getSignUpPage()


@app.route('/sign-out', methods=['POST'])
def signOut():
  return auth_controller.signOut()


if __name__ == '__main__':
  app.run()