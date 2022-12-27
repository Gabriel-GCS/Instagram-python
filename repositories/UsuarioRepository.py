import motor.motor_asyncio

from decouple import config

from models.UsuarioModel import UsuarioModel

MONGODB_URL = config("MONGODB_URL")

cliente = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = cliente.instagram

usuario_collection = database.get_collection("usuario")

async def criar_usuario(usuario: UsuarioModel) -> dict:
    usuario_criado = await usuario_collection.insert_one(usuario.__dict__)

    novo_usuario = await usuario_collection.find_onde({ '_id': usuario_criado.inserted_id})

    return{
        "nome":novo_usuario['nome'],
        "email": novo_usuario['email'],
        "senha": novo_usuario['senha'],
        "foto": novo_usuario['foto'],
    }