from functools import wraps
from flask import redirect, request, session
from urllib.parse import urlencode

def login_required(f):
  '''
  Redireciona o usuário para a tela de login se ele não estiver autenticado.
  
  Inclui na url do login o parâmetro :attr:`next`, correspondente à url atual,
  que poderá ser utilizada para redirecionar o usuário para a tela que ele
  estava tentando acessar antes de se autenticar.
  '''
  @wraps(f)
  def handle_login_required(*args, **kwargs):
    if 'id' not in session:
      params = urlencode({ 'next': request.url })
      return redirect(f'/sign-in?{params}')
    return f(*args, **kwargs)
  
  return handle_login_required


def unprotected_route(f):
  '''
  Redireciona o usuário para a tela inicial se ele já estiver autenticado.
  
  Útil para ser utilizado nas telas de cadastro, login, ou outra tela onde o 
  usuário não deve estar logado para conseguir acesso.
  '''
  @wraps(f)
  def handle_unprotected_route(*args, **kwargs):
    if 'id' in session:
      return redirect('/')
    return f(*args, **kwargs)
  
  return handle_unprotected_route