class Action:
  def __init__(self, id, symbol, name, shares, price):
    self.id = id
    self.symbol = symbol
    self.name = name
    self.shares = shares
    self.price = price

  @property
  def total(self):
    return self.price * self.shares