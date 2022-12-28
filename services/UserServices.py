from models.UserModel import UserModel
from repositories.UserRepository import create_user, update_user, list_users, list_by_email_user, list_user_id


async def create_user_service(user: UserModel):
    try:
        user_found = await list_by_email_user(user.email)

        if user_found['status'] != 400:
            return{
                "msg": "email already exists",
                "data": "",
                "status": 400
            }
        new_user = await create_user(user)

        return {
            "msg": "create user success",
            "data": new_user,
            "status": 200
        }
    except Exception as error:
        return {
            "msg": "internal error",
            "data": str(error),
            "status": 500
        }


async def found_user(user_id: str):
    try:
        user_found = await list_user_id(user_id)
        if not user_found:
            return {
                "msg": "user not found",
                "data": "",
                "status": 404
            }
        return user_found
    except Exception as error:
        return {
            "msg": "internal error",
            "data": str(error),
            "status": 500
        }
