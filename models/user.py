from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id: int, username: str, role: str, password_hash: str):
        self.id = id
        self.username = username
        self.role = role
        self.password_hash = password_hash

    @staticmethod
    def create_password_hash(password: str) -> str:
        return generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password) 