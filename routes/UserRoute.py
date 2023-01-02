from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile

from middlewares.JWTMiddleware import check_jwt_token
from models.UserModel import UserCreateModel
from services.AuthService import AuthService
from services.UserServices import UserService

userService = UserService()
authService = AuthService()
router = APIRouter()


@router.post("/", response_description='route to create new user')
async def create_user_route(file: UploadFile, user: UserCreateModel = Depends(UserCreateModel)):
    try:
        photo_route = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'

        with open(photo_route, 'wb+') as files:
            files.write(file.file.read())

        result = await userService.create_user_service(user, photo_route)

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

    decoded_token = authService.decode_jwt(token)

    user = await userService.found_user(decoded_token['user_id'])

    return user
