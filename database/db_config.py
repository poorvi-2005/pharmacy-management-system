import mysql.connector
from mysql.connector import Error
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    _instance = None
    _connection = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    database=os.getenv('DB_NAME', 'pharmacy_db'),
                    user=os.getenv('DB_USER', 'root'),
                    password=os.getenv('DB_PASSWORD', 'root'),
                    autocommit=True
                )
            except Error as e:
                print(f"Error connecting to database: {e}")
                raise
        return self._connection

    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close() 