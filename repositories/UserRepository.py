import motor.motor_asyncio
from bson import ObjectId

from decouple import config

from models.UserModel import UserModel
from utils.AuthUtil import password_encrypt

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.instagram

user_collection = database.get_collection("user")


def user_helper(user):
    return {
        "id": user["_id"],
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "photo": user["photo"] if "photo" in user else "",
    }


async def create_user(user: UserModel) -> dict:
    try:
        user.password = password_encrypt(user.password)
        user = await user_collection.insert_one(user.__dict__)

        new_user = await user_collection.find_one({'_id': user.inserted_id})

        return user_helper(new_user)
    except Exception as error:
        return {
            "msg": "Internal error",
            "data": str(error),
            "status": 500
        }


async def list_users():
    return user_collection.find()


async def list_by_email_user(email: str):
    user = await user_collection.find_one({'email': email})

    if not user:
        return {
                'msg': 'user not found',
                "data": "",
                "status": 404
        }
    return user_helper(user)


async def list_user_id(user_id: str):
    user = await user_collection.find_one({'_id': ObjectId(user_id)})

    if user:
        return user_helper(user)


async def update_user(user_id: str, data: dict):
    try:
        user = await user_collection.find_one({'_id': ObjectId(user_id)})

        if not user:
            return {
                'msg': 'user not found',
                "data": "",
                "status": 404
            }
        updated_user = await user_collection.update_one(
            {'_id': ObjectId(user_id)}, {"$set": data}
        )

        return user_helper(updated_user)
    except Exception as error:
        return {
            "msg": "internal error",
            "data": str(error),
            "status": 500
        }


async def delete_user(user_id: str):
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
