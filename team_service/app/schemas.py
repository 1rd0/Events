from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Схема для чтения участника
class TeamMemberRead(BaseModel):
    id: int
    team_id: int
    user_id: int
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True

# Схемы для команд
class TeamBase(BaseModel):
    name: str
    captain_id: int

class TeamCreate(TeamBase):
    pass
class TeamRead(TeamBase):
    id: int
    created_at: datetime
    members: list[TeamMemberRead] = []  # Список участников команды

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True
# Схема для добавления участника
class TeamMemberCreate(BaseModel):
    team_id: int
    user_id: int
    role: Optional[str] = "player"

 