# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic_settings import SettingsConfigDict  # Для Pydantic 2.x
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
# Схемы для пользователей
class UserBase(BaseModel):
    email: str = Field(..., description="Email пользователя")
    full_name: Optional[str] = Field(None, description="Полное имя пользователя")

class UserCreate(UserBase):
    password: str = Field(..., description="Пароль пользователя")

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Для работы с Pydantic ORM mode

# Схемы для команд
class TeamBase(BaseModel):
    name: str
    captain_id: Optional[int] = None

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: int
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)

# Схемы для регистраций
class RegistrationBase(BaseModel):
    team_id: int
    tournament_id: int

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationRead(RegistrationBase):
    id: int
    status: str
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)
