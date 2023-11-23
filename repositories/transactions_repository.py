import sqlite3
from database import dbconnection
from entities.transaction import Action, Transaction
from datetime import datetime

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
