import mysql.connector
from datetime import datetime

def connect(
  user: str, 
  password: str, 
  host: str="localhost"
) -> mysql.connector.connection_cext.CMySQLConnection:
  cnx = mysql.connector.connect(
    user=user,
    password=password,  # TODO: Make this a CLI argument
    host=host,
    database="exhibitioninference"
  )
  return cnx


def insert_into_tag_data(
  cnx: mysql.connector.connection_cext.CMySQLConnection,
  tagId: int,
  ts: str, # ISO 8601
  x: float,
  y: float,
  z: float,
  quality: int
) -> bool:
  try:
    cursor = cnx.cursor()
    cursor.execute(
      """INSERT IGNORE INTO tag_data VALUES (%s, %s, %s, %s, %s, %s)""",  # IGNORE is added for idempotence
      (tagId, datetime.fromisoformat(ts), x, y, z, quality)
    )
    cnx.commit()
    return True
  except Exception:
    return False
  finally:
    cursor.close()


# This is just for demonstration, needs to be tailored to our use case
def prototype_query(
  cnx: mysql.connector.connection_cext.CMySQLConnection,
  ts_start: datetime=datetime(2022, 2, 20, 15, 0, 0, 0),
  ts_end: datetime=datetime(2022, 2, 28, 15, 0, 0, 0)
) -> any:
  cursor = cnx.cursor()
  cursor.execute(
      """SELECT * FROM tag_data WHERE timestamp BETWEEN %s AND %s""",
      (ts_start, ts_end)
  )
  result = [e for e in cursor]
  cursor.close()
  return result