from fastapi import APIRouter, Body

from models.UsuarioModel import UsuarioModel
from repositories.UsuarioRepository import criar_usuario

router = APIRouter()

@router.post("/", response_description='rota para criar um novo usuario')
async def criarUsuario(usuario: UsuarioModel = Body(...)):

    resultado = await criar_usuario(usuario)

    return resultado