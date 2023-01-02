from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, EmailStr


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


class UserModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: str = Field(...)
    token: str

    class Config:
        schema_extra = {
            "usuario": {
                "name": "string",
                "email": "string",
                "password": "string",
                "photo": "string",
            }
        }
@form_body
class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "name": "Gabriel",
                "email": "gabriel@hotmail.com",
                "password": "123gabriel",
            }
        }


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "email": "gabriel@hotmail.com",
                "password": "123gabriel",
            }
        }

@form_body
class UpdateUserModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: UploadFile = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "name": "teste",
                "email": "teste@gmail.com",
                "password": "123Teste",
                "photo": "teste.png",
            }
        }
