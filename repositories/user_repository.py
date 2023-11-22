import sqlite3
import database.dbconnection as dbconnection
from entities.user import UserCreateDTO

def createUser(user: UserCreateDTO):
  '''
  Cadastra um novo usuário no banco de dados.
  :param user: Usuário a ser cadastrado
  '''
  with dbconnection.connect() as con:
    try:
      id = con.execute(
        'INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?);',
        (
          user.id,
          user.name,
          user.email,
          user.password_hash,
        )
      )
      return id
    except sqlite3.IntegrityError as error:
      for message in error.args:
        if 'users.email' in message:
          raise Exception('email already exists') 
      raise Exception('unexpected error')
    except:
      raise Exception('unexpected error')