from typing import Optional
from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    firstName: str
    lastName: str
    email: EmailStr
    role: str
    password: str
    contactNumber: str
    address: Optional[list] = None

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "password": "3xt3m#",
            }
        }

    class Settings:
        name = "admin"


class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "abdul@youngest.dev", "password": "3xt3m#"}
        }


class UserData(BaseModel):
    fullname: str
    email: EmailStr
    address: Optional[list] = None