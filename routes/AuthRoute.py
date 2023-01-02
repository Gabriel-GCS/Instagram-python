from fastapi import APIRouter, Body, HTTPException

from models.UserModel import UserCreateModel, UserLogin
from services.AuthService import AuthService

authService = AuthService()
router = APIRouter()


@router.post("/login", response_description='route to login user')
async def login_route(user: UserLogin = Body(...)):
    result = authService.login_service(user)

    if not result['status'] == 200:
        raise HTTPException(status_code=result['status'], detail=result['msg'])

    del result['date']['password']

    token = authService.jwt_generate(result['date']['id'])

    result['token'] = token

    return result
