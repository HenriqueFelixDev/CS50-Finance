import datetime

def usd(value: float):
  """
  Formata o :attr:`value` de acordo com a representação do dólar 
  com 2 casas decimais
  """
  return f'$ {value:,.2f}'


def date(date: datetime):
  """
  Formata a data no padrão MMM dd, YYYY. ex: Jun 10, 2020
  :param date: A data a ser formatada
  """
  return date.strftime('%b %d, %Y')


def datetime(date: datetime):
  """
  Formata a data no padrão MMM dd, YYYY HH:mm. ex: Jun 10, 2020, 10:18
  :param date: A data a ser formatada
  """
  return date.strftime('%b %d, %Y %H:%M')