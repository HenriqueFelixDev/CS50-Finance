import sqlite3
from database import dbconnection
from entities.transaction import Action

def getActiveActions(userId: str) -> list[Action]:
  with dbconnection.connect() as con:
    con.row_factory = sqlite3.Row

    result = con.execute(
      '''
      SELECT
        id,
        symbol,
        name,
        SUM(
          CASE WHEN (operation = 'buy')
          THEN shares
          ELSE -shares
          END
        ) as total_shares
      FROM transactions
      WHERE user_id = :user_id
      GROUP BY symbol
      HAVING total_shares > 0;
      ''',
      {'user_id': userId}
    )

    items = []

    for row in result.fetchall():
      action = Action(
        id=row['id'],
        symbol=row['symbol'],
        name=row['name'],
        shares=row['total_shares'],
        price=0.0,
      )

      items.append(action)

    return items