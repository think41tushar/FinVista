from passlib.context import CryptContext
from data.user_dao import get_user_by_email, create_user
from datetime import datetime

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def login_or_signup(email: str, password: str):
    user = get_user_by_email(email)
    if user:
        if not pwd_ctx.verify(password, user["hashed_password"]):
            raise Exception("Invalid credentials")
        return user
    # signup
    hashed = pwd_ctx.hash(password)
    return create_user(email, hashed)