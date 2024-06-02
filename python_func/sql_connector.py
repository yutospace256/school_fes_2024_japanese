import sqlite3

class SqliteConnector:
  def __init__(self, database_path):
    self.connection = sqlite3.connect(database_path)
    self.cursor = self.connection.cursor()

  def __enter__(self):
    return self  # Return itself for use within the with block

  def __exit__(self, exc_type, exc_val, exc_tb):
      if exc_type is not None:
          self.connection.rollback()  # Rollback if an exception occurs
      self.close()  # Close the connection in any case

  def fetch_data(self, query, values=()):
    self.cursor.execute(query, values)
    results = self.cursor.fetchall()
    return results

  def update_data(self, query, values):
    self.cursor.execute(query, values)
    self.connection.commit()

  def insert_data(self, query, values):
    self.cursor.execute(query, values)
    self.connection.commit()

  def delete_data(self, query, values):
    self.cursor.execute(query, values)
    self.connection.commit()

  def execute_query(self, query, values=()):
    self.cursor.execute(query, values)

  def close(self):
    self.cursor.close()
    self.connection.close()

  def fetchone(self):
    return self.cursor.fetchone()
