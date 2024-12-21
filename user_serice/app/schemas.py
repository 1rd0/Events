# app/schemas.py

from pydantic import BaseModel 
from typing import Optional
from datetime import datetime
from pydantic_settings import SettingsConfigDict  # Для Pydantic 2.x

# Схемы для пользователей
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)  # Включение ORM-режима

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
