from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile

from middlewares.JWTMiddleware import check_jwt_token
from models.UserModel import UserModel
from services.AuthService import decode_jwt
from services.UserServices import create_user_service, found_user

router = APIRouter()


@router.post("/", response_description='route to create new user')
async def create_user_route(file: UploadFile, user: UserModel = Depends(UserModel)):
    try:
        result = await create_user_service(user)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['msg'])

        return result
    except Exception as error:
        raise error

@router.get(
    "/me",
    response_description='route to list user info',
    dependencies=[Depends(check_jwt_token)]
)
async def list_logged_user(auth: str = Header(default='')):
    token = auth.split(' ')[1]

    decoded_token = decode_jwt(token)

    user = await found_user(decoded_token['user_id'])

    return user
