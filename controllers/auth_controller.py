from flask import request, render_template, redirect, session, flash, get_flashed_messages
from cuid2 import Cuid
import bcrypt
from entities.user import UserCreateDTO
from repositories.user_repository import createUser, getUserByEmail
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
    session['funds'] = 10000
    
    return redirect('/')
  except Exception as error:
    flash(message=error, category='error')
    return getSignUpPage()


def signIn():
  '''
  Realiza a autenticação do usuário pelo email e senha.

  Ao receber a requisição realiza a validação do formulário por meio da classe
  :class:`~core.validators.UserSignInValidator`. Se algum dos campos estiver com
  valores inválidos retorna a página de login com um erro debaixo de cada campo
  inválido.

  Após a validação é realizada a consulta no banco de dados pelo usuário com o
  e-mail informado. O hash da senha do usuário encontrado no banco de dados é 
  comparado com a senha informada no formulário. Caso nenhum usuário com o
  e-mail informado seja encontrado no banco de dados ou caso as senhas não 
  coincidam, retorna à tela de login com a mensagem de erro 'user not found'.

  Caso ocorra tudo certo os dados do usuário são salvos em uma sessão e ele é 
  redirecionado para a url do parâmetro :attr:`next`, caso exista, senão, é 
  redirecionado para a tela inicial da aplicação
  '''
  form = UserSignInValidator(request.form)

  if not form.validate():
    return getSignInPage(form)
    
  email = form.email.data
  password = form.password.data

  try:
    user = getUserByEmail(email)

    passwordMatches = False

    if user is not None:
      passwordMatches = bcrypt.checkpw(
        bytes(password, 'utf-8'),
        user.password_hash,
      )

    if user is None or not passwordMatches:
      flash(message='user not found', category='error')
      return getSignInPage(form)

    session['id'] = user.id
    session['name'] = user.name
    session['email'] = user.email
    session['funds'] = user.funds

    if 'next' in request.args:
      route = request.args['next']
      return redirect(route)
    
    return redirect('/')

    
  except Exception as error:
    flash(message=error, category='error')
    return getSignInPage(form)


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