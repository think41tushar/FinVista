from passlib.context import CryptContext
from data.user_dao import get_user_by_email, create_user
from utils.security import create_access_token

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_or_register(email: str, password: str):
    user = get_user_by_email(email)
    if user:
        if not pwd_ctx.verify(password, user["hashed_password"]):
            raise Exception("Invalid credentials")
    else:
        hashed = pwd_ctx.hash(password)
        user = create_user(email, hashed)

    token = create_access_token(
        data={"sub": user["email"]},
    )
    del user["hashed_password"]
    return {"access_token": token, "token_type": "bearer", **user}