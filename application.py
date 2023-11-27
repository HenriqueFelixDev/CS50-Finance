from flask import Flask, request
from flask_session import Session
from core import filters, decorators
from controllers import auth_controller, history_controller, index_controller, quote_controller
import datetime
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Injeta globalmente a variável current_date para que seja acessível de todos
# os templates
@app.context_processor
def inject_globals():
    return { 'current_date': datetime.datetime.now() }


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


@app.route('/actions/buy', methods=['POST'])
@decorators.login_required
def actions():
  return index_controller.buyAction()


@app.route('/sign-in', methods=['GET', 'POST'])
@decorators.unprotected_route
def signIn():
  if request.method == 'POST':
    return auth_controller.signIn()
  
  return auth_controller.getSignInPage()


@app.route('/sign-up', methods=['GET', 'POST'])
@decorators.unprotected_route
def signup():
  if request.method == 'POST':
    return auth_controller.signUp()
  
  return auth_controller.getSignUpPage()


@app.route('/sign-out', methods=['POST'])
def signOut():
  return auth_controller.signOut()


@app.route('/quotes', methods=['GET', 'POST'])
def quotes():
  if request.method == 'POST':
    return quote_controller.getQuotes()
  
  return quote_controller.getQuotesPage()


@app.route('/history', methods=['GET'])
def history():
  return history_controller.getHistoryPage()


if __name__ == '__main__':
  app.run()