from fastapi import Form
from pydantic import BaseModel, Field, EmailStr


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class UserModel(BaseModel):
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
