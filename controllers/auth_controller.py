from flask import request, render_template, redirect, session, flash, get_flashed_messages
from cuid2 import Cuid
import bcrypt
from entities.user import UserCreateDTO
from repositories.user_repository import createUser
from core.validators import UserCreateValidator, UserSignInValidator

def signUp():
  '''
  Cadastra um usuário no banco de dados.
  
  Após receber os dados da requisição, realiza a validação dos campos com 
  a classe :class:`core.validators.UserCreateValidator`.

  Se os campos estiverem com valores inválidos, retorna à página de cadastro
  exibindo as mensagens de erro em cada campo.

  Se os campos estiverem com valores válidos, cria um hash da senha do usuário,
  cria um CUID (sequência de caracteres única) que será utilizado no id do 
  usuário e instancia um novo :class:`~entities.user.UserCreateDTO`.

  Cadastra um novo usuário no banco de dados com a função 
  :func:`~repositories.user_repository.createUser`, salva as informações do
  usuário criado em uma sessão para autenticação e o redireciona para a tela
  index.

  Se ocorrer um erro em alguma etapa da criação de conta, a tela de cadastro é 
  exibida novamente com uma mensagem informando o erro.
  '''
  form = UserCreateValidator(request.form)

  if not form.validate():
    return getSignUpPage(form)

  try:
    password_hash = bcrypt.hashpw(
      bytes(form.password.data, 'utf-8'),
      bcrypt.gensalt(),
    )

    user = UserCreateDTO(
      id = Cuid().generate(),
      name = form.name.data,
      email = form.email.data,
      password_hash = password_hash
    )

    createUser(user)

    session['id'] = user.id
    session['name'] = user.name
    session['email'] = user.email
    
    return redirect('/')
  except Exception as error:
    flash(message=error, category='error')
    return getSignUpPage()


def signIn():
  form = UserSignInValidator(request.form)

  if not form.validate():
    return getSignInPage(form)
  
  return redirect('/')


def signOut():
  '''
  Desloga o usuário do sistema
  '''
  session.clear()

  return redirect('/sign-in')


def getSignUpPage(form = {
  'name': None,
  'email': None,
  'password': None,
  'confirm_password': None,
}):
  '''
  Exibe a tela de cadastro.

  Se qualquer erro ocorrer durante o processo de cadastro do usuário, a 
  propriedade :attr:`request.form` estará preenchida com os valores digitados 
  pelo usuário. Esses valores são injetados no template para que os campos 
  já apareçam preenchidos com os valores digitados anteriormente pelo usuário, 
  permitindo-o alterá-los sem ter que digitar tudo novamente.
  '''

  return render_template('pages/signup.html', form=form)


def getSignInPage(form = {
  'email': None,
  'password': None,
}):
  '''
  Exibe a tela de login.

  Se qualquer erro ocorrer durante o processo de login do usuário, a 
  propriedade :attr:`request.form` estará preenchida com os valores digitados 
  pelo usuário. Esses valores são injetados no template para que os campos 
  já apareçam preenchidos com os valores digitados anteriormente pelo usuário, 
  permitindo-o alterá-los sem ter que digitar tudo novamente.
  '''

  return render_template('pages/signin.html', form=form)