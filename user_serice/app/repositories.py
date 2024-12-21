# app/repositories.py

from typing import Optional, List
from tortoise.exceptions import DoesNotExist, IntegrityError
from app.models import User, Team, Registration
from app.schemas import UserCreate, TeamCreate, RegistrationCreate

class UserRepository:
    @staticmethod
    async def create_user(user: UserCreate) -> User:
        try:
            user_obj = await User.create(**user.model_dump())
            return user_obj
        except IntegrityError:
            raise ValueError("Пользователь с таким email уже существует")

    @staticmethod
    async def get_user(user_id: int) -> Optional[User]:
        return await User.get_or_none(id=user_id)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        return await User.get_or_none(email=email)

class TeamRepository:
    @staticmethod
    async def create_team(team: TeamCreate) -> Team:
        if team.captain_id:
            captain = await User.get_or_none(id=team.captain_id)
            if not captain:
                raise ValueError("Капитан не найден")
        team_obj = await Team.create(name=team.name, captain_id=team.captain_id)
        return team_obj

    @staticmethod
    async def get_team(team_id: int) -> Optional[Team]:
        return await Team.get_or_none(id=team_id)

class RegistrationRepository:
    @staticmethod
    async def create_registration(registration: RegistrationCreate) -> Registration:
        team = await Team.get_or_none(id=registration.team_id)
        if not team:
            raise ValueError("Команда не найдена")
        registration_obj = await Registration.create(
            team_id=registration.team_id,
            tournament_id=registration.tournament_id,
            status="pending"
        )
        return registration_obj

    @staticmethod
    async def get_registration(registration_id: int) -> Optional[Registration]:
        return await Registration.get_or_none(id=registration_id)
