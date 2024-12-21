from tortoise.exceptions import DoesNotExist
from app.models import Team, Registration
from app.schemas import TeamCreate, RegistrationCreate
from app.models import TeamMember
from app.schemas import TeamMemberCreate

class TeamMemberRepository:
    @staticmethod
    async def add_member(member: TeamMemberCreate) -> TeamMember:
        return await TeamMember.create(**member.dict())

    @staticmethod
    async def get_members_by_team(team_id: int):
        return await TeamMember.filter(team_id=team_id).all()

class TeamRepository:
    @staticmethod
    async def create_team(team: TeamCreate) -> Team:
        team_obj = await Team.create(**team.dict())
        return team_obj

    @staticmethod
    async def get_team(team_id: int):
        return await Team.get_or_none(id=team_id)

class RegistrationRepository:
    @staticmethod
    async def create_registration(registration: RegistrationCreate) -> Registration:
        return await Registration.create(**registration.dict())

    @staticmethod
    async def get_registration(registration_id: int):
        return await Registration.get_or_none(id=registration_id)
import httpx
from fastapi import HTTPException

class TournamentServiceClient:
    BASE_URL = "http://localhost:8004"  # Замените на адрес Tournament Service

    @staticmethod
    async def check_tournament_exists(tournament_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TournamentServiceClient.BASE_URL}/tournaments/{tournament_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Турнир не найден")
            elif response.status_code != 200:
                raise HTTPException(status_code=500, detail="Ошибка проверки турнира")
 
class UserServiceClient:
    BASE_URL = "http://localhost:8005"  # URL User Service

    @staticmethod
    async def check_user_exists(user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{UserServiceClient.BASE_URL}/users/{user_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} не найден")
            elif response.status_code != 200:
                raise HTTPException(status_code=500, detail="Ошибка при проверке пользователя")
