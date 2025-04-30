import sqlite3
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e} at {self.db_path}")

    def close(self):
        if self.conn:
            self.conn.close()

    def load_table(self, table_name):
        if self.conn is None:
            print("No database connection found.")
            return pd.DataFrame()

        try:
            return pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        except Exception as e:
            print(f"Failed to load {table_name}: {e}")
            return pd.DataFrame()

    def query_from_table(self, table_name, condition=None):
        if self.conn is None:
            print("No database connection found.")
            return pd.DataFrame()

        try:
            query = f"SELECT * FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            print(f"Failed to load {table_name} with condition '{condition}': {e}")
            return pd.DataFrame()

    def extract_base_table(self, table_name="wards", condition=None):
        """
        Extract a base table from the database and return it as a DataFrame.
        """
        self.connect()
        if self.conn and condition is None:
            base_table = self.load_table(table_name)
            self.close()
            return base_table
        elif self.conn and condition is not None:
            base_table = self.query_from_table(table_name, condition)
            self.close()
            return base_table
        return pd.DataFrame()

