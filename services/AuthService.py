import jwt
from decouple import config

from models.UserModel import UserLogin
from services.UserServices import UserService
from utils.AuthUtil import AuthUtil
import time

userService = UserService()
authUtils = AuthUtil()

JWT_SECRET = config('JWT_SECRET')

class AuthService:
    def jwt_generate(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "time_expiration": time.time() + 6000
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return token

    def decode_jwt(self, token: str):
        try:
            decode_token = jwt.decode(token, JWT_SECRET, algorithm="HS256")
            if decode_token['time_expiration'] >= time.time():
                return decode_token
            return None
        except Exception as error:
            print(error)
            return None

    async def login_service(self, user: UserLogin):
        user_found = await userService.list_by_email_user(user.email)

        if not user_found:
            return {
                'msg': 'Email or password incorrect',
                "data": "",
                "status": 401
            }
        if not authUtils.check_password(user.password, user_found['password']):
            return {
                'msg': 'Email or password incorrect',
                "data": "",
                "status": 401
            }
        return {
            'msg': 'Login success',
            "data": "",
            "status": 200
        }
