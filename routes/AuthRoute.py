from fastapi import APIRouter, Body, HTTPException

from models.UserModel import UserModel, UserLogin
from services.AuthService import login_service, jwt_generate

router = APIRouter()


@router.post("/login", response_description='route to login user')
async def login_route(user: UserLogin = Body(...)):
    result = login_service(user)

    if not result['status'] == 200:
        raise HTTPException(status_code=result['status'], detail=result['msg'])

    del result['date']['password']

    token = jwt_generate(result['date']['id'])

    result['token'] = token

    return result
