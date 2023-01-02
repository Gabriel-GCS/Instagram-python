from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


class AuthUtil:
    def password_encrypt(self, password: str):
        return pwd_context.hash(password)

    def check_password(self, password: str, password_encrypted):
        return pwd_context.verify(password, password_encrypted)
