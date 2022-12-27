from pydantic import BaseModel, Field, EmailStr

class UsuarioModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    nome: str = Field(...)
    foto: str = Field(...)

class Config:
    schema_extra = {
        "usuario": {
            "nome":"Gabriel",
            "email": "gabriel@hotmail.com",
            "senha": "123gabriel",
            "nome": "gabriel.png",
        }
    }