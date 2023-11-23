class Action:
  def __init__(self, symbol, name, shares, price):
    self.symbol = symbol
    self.name = name
    self.shares = shares
    self.price = price

  @property
  def total(self):
    return self.price * self.shares