from typing import List, Optional, TypeVar, Generic
from mysql.connector import Error
from ..database.db_config import DatabaseConfig

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self):
        self.db = DatabaseConfig.get_instance()

    def execute_query(self, query: str, params: tuple = None) -> Optional[int]:
        connection = self.db.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            if cursor.lastrowid:
                return cursor.lastrowid
            return None
        except Error as e:
            print(f"Error executing query: {e}")
            connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def fetch_one(self, query: str, params: tuple = None) -> Optional[tuple]:
        connection = self.db.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching one: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query: str, params: tuple = None) -> List[tuple]:
        connection = self.db.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching all: {e}")
            raise
        finally:
            if cursor:
                cursor.close() 