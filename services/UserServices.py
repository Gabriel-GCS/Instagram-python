from models.UserModel import UserCreateModel, UpdateUserModel
from repositories.UserRepository import UserRepository
from providers.AWSProvider import AWSProvider

awsProvider = AWSProvider()
userRepository = UserRepository()


class UserService:
    async def create_user_service(self, user: UserCreateModel, photo_route):
        try:
            user_found = await userRepository.list_by_email_user(user.email)

            if user_found:
                return{
                    "msg": "email already exists",
                    "data": "",
                    "status": 400
                }
            new_user = await userRepository.create_user(user)
            try:
                url_photo = awsProvider.upload_file_s3(
                    f'photo-profile/{new_user["id"]}.png',
                    photo_route
                )
                new_user_update = await userRepository.update_user(new_user["id"], {"photo": url_photo})
            except Exception as error:
                print(error)

            return {
                "msg": "user created success",
                "data": new_user_update,
                "status": 201
            }
        except Exception as error:
            return {
                "msg": "internal error",
                "data": str(error),
                "status": 500
            }

    async def found_user(self, user_id: str):
        try:
            user_found = await userRepository.list_user_id(user_id)
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

    async def update_user(self, user_id: str, update_user_date: UpdateUserModel):

