from fastapi import Header, HTTPException

from services.AuthService import AuthService

authService = AuthService()


async def check_jwt_token(auth: str = Header(default='')):
    if not auth.split(' ')[0] == 'Bearer':
        raise HTTPException(status_code=401, detail='invalid token')

    token = auth.split(' ')[1]
    payload = authService.decode_jwt(token)

    if not payload:
        raise HTTPException(status_code=401, detail='invalid token or expired')
    return payload
