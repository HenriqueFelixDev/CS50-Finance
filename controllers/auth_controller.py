from flask import request, render_template, redirect, session, flash, get_flashed_messages
from cuid2 import Cuid
import bcrypt
from entities.user import UserCreateDTO
from repositories.user_repository import createUser
from core.validators import UserCreateValidator

def signUp():
  form = UserCreateValidator(request.form)

  if not form.validate():
    return getSignUpPage()

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


def getSignUpPage():
  form = {
    'name': request.form.get('name'),
    'email': request.form.get('email'),
    'password': request.form.get('password'),
    'confirm_password': request.form.get('confirm_password'),
  }

  return render_template('pages/signup.html', form=form)