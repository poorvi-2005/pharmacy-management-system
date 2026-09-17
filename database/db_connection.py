import mysql.connector
from mysql.connector import Error
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        if not self.connection:
            try:
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    database=os.getenv('DB_NAME', 'pharmacy_db'),
                    user=os.getenv('DB_USER', 'root'),
                    password=os.getenv('DB_PASSWORD', 'root')
                )
                print("Successfully connected to the database")
            except Error as e:
                print( 