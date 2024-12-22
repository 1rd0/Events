from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from pydantic_settings import SettingsConfigDict

class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date

class TournamentCreate(TournamentBase):
    pass

class TournamentRead(TournamentBase):
    id: int
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)
class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
class GameBase(BaseModel):
    name: str
    tournament_id: int
    scheduled_at: datetime

class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: int
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)
