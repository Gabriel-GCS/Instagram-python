import jwt
from decouple import config

from models.UserModel import UserLogin
from services.UserServices import list_by_email_user
from utils.AuthUtil import check_password
import time

JWT_SECRET = config('JWT_SECRET')


def jwt_generate(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "time_expiration": time.time() + 6000
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return token


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm="HS256")
        if decode_token['time_expiration'] >= time.time():
            return decode_token
        return None
    except Exception as error:
        print(error)
        return None



async def login_service(user: UserLogin):
    user_found = await list_by_email_user(user.email)

    if not user_found:
        return {
            'msg': 'Email or password incorrect',
            "data": "",
            "status": 401
        }
    if not check_password(user.password, user_found['password']):
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
