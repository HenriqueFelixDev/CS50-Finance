class User:
  def __init__(self, id, name, email, password_hash, funds, created_at):
    self.id = id
    self.name = name
    self.email = email
    self.password_hash = password_hash
    self.funds = funds
    self.created_at = created_at


class UserCreateDTO:
  def __init__(self, id, name, email, password_hash):
    self.id = id
    self.name = name
    self.email = email
    self.password_hash = password_hash


class UserSignInDTO:
  def __init__(self, email, password):
    self.email = email
    self.password = password