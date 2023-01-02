import motor.motor_asyncio
from bson import ObjectId

from decouple import config
from utils.ConverterUtil import ConverterUtil
from models.UserModel import UserCreateModel, UserModel
from utils.AuthUtil import AuthUtil

converterUtil = ConverterUtil()
authUtil = AuthUtil()

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.instagram

user_collection = database.get_collection("user")


class UserRepository:
    async def create_user(self, user: UserCreateModel) -> UserModel:
        try:
            user.password = authUtil.password_encrypt(user.password)
            user_dict = {
                "name": user.name,
                "email": user.name,
                "password": user.password,
            }

            user = await user_collection.insert_one(user_dict)

            new_user = await user_collection.find_one({'_id': user.inserted_id})

            return converterUtil.user_helper(new_user)

        except Exception as error:
            return {
                "msg": "Internal error",
                "data": str(error),
                "status": 500
            }

    async def list_users(self):
        return user_collection.find()

    async def list_by_email_user(self, email: str):
        user = await user_collection.find_one({'email': email})

        if user:
            return converterUtil.user_helper(user)

    async def list_user_id(self, user_id: str):
        user = await user_collection.find_one({'_id': ObjectId(user_id)})

        if user:
            return converterUtil.user_helper(user)

    async def update_user(self, user_id: str, data: dict) -> UserModel:
        if['password'] in data:
            data['password'] = authUtil.password_encrypt(data['password'])
        try:
            user = await user_collection.find_one({"_id": ObjectId(user_id)})

            if user:
                await user_collection.update_one(
                    {"_id": ObjectId(user_id)}, {"$set": data}
                )
                user_found = await user_collection.find_one({
                    "_id": ObjectId(id)
                })

            return converterUtil.user_helper(user_found)
        except Exception as error:
            return {
                "msg": "internal error",
                "data": str(error),
                "status": 500
            }

    async def delete_user(self, user_id: str):
        try:
            user = await user_collection.find_one({'_id': ObjectId(user_id)})

            if not user:
                return {
                    'msg': 'user not found',
                    "data": "",
                    "status": 404
                }
            await user_collection.delete_one({'_id': ObjectId(user_id)})
            return{
                "msg": "deleted user success",
                "data": "",
                "status": 200
            }
        except Exception as error:
            return {
                "msg": "internal error",
                "data": str(error),
                "status": 500
            }
