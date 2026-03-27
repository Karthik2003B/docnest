from fastapi import HTTPException
from repositories.user_repository import UserRepository
from utils.security import hash_password, verify_password


class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def register_user(self, name: str, email: str, password: str):
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        password_hash = hash_password(password)
        return self.user_repo.create_user(name, email, password_hash)

    def login_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user