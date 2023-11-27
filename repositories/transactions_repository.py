import sqlite3
from database import dbconnection
from entities.transaction import Action, ActionCreateDTO, Transaction
from datetime import datetime

def buyAction(action: ActionCreateDTO):
  with dbconnection.connect() as con:
    con.row_factory = sqlite3.Row

    con.isolation_level = None
    cursor = con.cursor()

    cursor.execute('begin')

    try:
      cursor.execute(
        'UPDATE users SET funds = funds - ? WHERE id = ?;',
        (
          action.fundsDiscount,
          action.userId,
        ),
      )

      cursor.execute(
        '''
        INSERT INTO transactions (id, symbol, name, shares, price, user_id, operation)
        VALUES (?, ?, ?, ?, ?, ?, 'buy');
        ''',
        (
          action.id,
          action.symbol,
          action.name,
          action.shares,
          action.price,
          action.userId,
        ),
      )
      cursor.execute('commit')
    except:
      cursor.execute('rollback')


def sellAction(action: ActionCreateDTO):
  with dbconnection.connect() as con:
    con.row_factory = sqlite3.Row

    con.isolation_level = None
    cursor = con.cursor()

    cursor.execute('begin')

    try:
      cursor.execute(
        'UPDATE users SET funds = funds + ? WHERE id = ?;',
        (
          action.fundsDiscount,
          action.userId,
        ),
      )

      cursor.execute(
        '''
        INSERT INTO transactions (id, symbol, name, shares, price, user_id, operation)
        VALUES (?, ?, ?, ?, ?, ?, 'sell');
        ''',
        (
          action.id,
          action.symbol,
          action.name,
          action.shares,
          action.price,
          action.userId,
        ),
      )
      cursor.execute('commit')
    except:
      cursor.execute('rollback')


def getActiveActions(userId: str) -> list[Action]:
  with dbconnection.connect() as con:
    con.row_factory = sqlite3.Row

    result = con.execute(
      '''
      SELECT
        symbol,
        name,
        SUM(
          CASE WHEN (operation = 'buy')
          THEN shares
          ELSE -shares
          END
        ) as total_shares
      FROM transactions
      WHERE user_id = ?
      GROUP BY symbol
      HAVING total_shares > 0;
      ''',
      (userId,),
    )

    items = []

    for row in result.fetchall():
      action = Action(
        symbol=row['symbol'],
        name=row['name'],
        shares=row['total_shares'],
        price=0.0,
      )

      items.append(action)

    return items


def getActionBySymbol(symbol, userId: str) -> Action:
  with dbconnection.connect() as con:
    con.row_factory = sqlite3.Row

    result = con.execute(
      '''
      SELECT
        symbol,
        name,
        SUM(
          CASE WHEN (operation = 'buy')
          THEN shares
          ELSE -shares
          END
        ) as total_shares
      FROM transactions
      WHERE symbol = ? AND user_id = ?
      GROUP BY symbol
      HAVING total_shares > 0;
      ''',
      (symbol, userId,),
    )

    row = result.fetchone()

    if row is None:
      return None

    return Action(
      symbol=row['symbol'],
      name=row['name'],
      shares=row['total_shares'],
      price=0.0,
    )


def getAllTransactions(userId: str) -> list[Transaction]:
  with dbconnection.connect() as con:
    con.row_factory = sqlite3.Row
    
    result = con.execute(
      '''
      SELECT * FROM transactions
      WHERE user_id = ?
      ORDER BY datetime DESC;
      ''',
      (userId,),
    )

    items = []

    for row in result.fetchall():
      transaction = Transaction(
        id=row['id'],
        symbol=row['symbol'],
        name=row['name'],
        shares=row['shares'],
        price=row['price'],
        operation=row['operation'],
        datetime=datetime.fromisoformat(row['datetime']),
      )

      items.append(transaction)
    
    return items
