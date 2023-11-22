from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr

class AdminSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {"username": "abdul@youngest.dev", "password": "3xt3m#"}
        }


class AdminData(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    role: str
    password: str
    contactNumber: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
            }
        }

class AdminDataOut(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    role: str
    contactNumber: str