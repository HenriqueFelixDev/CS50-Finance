import sqlite3
import database.dbconnection as dbconnection
from entities.user import UserCreateDTO, User

def createUser(user: UserCreateDTO) -> str:
  '''
  Cadastra um novo usuário no banco de dados.
  :param user: Usuário a ser cadastrado
  :return: :attr:`id` do usuário criado
  '''
  with dbconnection.connect() as con:
    try:
      con.execute(
        'INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?);',
        (
          user.id,
          user.name,
          user.email,
          user.password_hash,
        )
      )
      return user.id
    except sqlite3.IntegrityError as error:
      for message in error.args:
        if 'users.email' in message:
          raise Exception('email already exists') 
      raise Exception('unexpected error')
    except:
      raise Exception('unexpected error')


def getUserByEmail(email: str) -> User:
  '''
  Retorna um usuário cadastrado no banco de dados pelo seu email

  :param email: E-mail do usuário a ser consultado
  :return: Usuário associado ao e-mail ou ``None``, caso não encontre
  '''
  with dbconnection.connect() as con:
    try:
      con.row_factory = sqlite3.Row
      cursor = con.execute('SELECT * FROM users WHERE email=?', (email,))

      result = cursor.fetchone()

      if result is None:
        return None
      
      return User(
        result['id'],
        result['name'],
        result['email'],
        result['password_hash'],
        result['funds'],
        result['created_at']
      )
    except:
      raise Exception('unexpected error')