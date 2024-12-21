from pydantic import BaseModel, EmailStr

class UserCreatedMessage(BaseModel):
    email: EmailStr
    full_name: str
