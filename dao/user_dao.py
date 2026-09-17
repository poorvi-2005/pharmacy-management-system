from typing import Optional
from mysql.connector import Error
from ..database.db_connection import DatabaseConnection
from ..models.user import User

class UserDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            
            result = cursor.fetchone()
            if result:
                return User(
                    id=result[0],
                    username=result[1],
                    role=result[2],
                    password_hash=result[3]
                )
            return None
        except Error as e:
            print(f"Error retrieving user: {e}")
            return None
        finally:
            if cursor:
                cursor.close() 