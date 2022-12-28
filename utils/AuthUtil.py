from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def password_encrypt(password: str):
    return pwd_context.hash(password)


def check_password(password: str, password_encrypted):
    return pwd_context.verify(password, password_encrypted)