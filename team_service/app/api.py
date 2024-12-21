from fastapi import APIRouter, HTTPException
from app import schemas, repositories
from app.repositories import TeamMemberRepository,TournamentServiceClient,UserServiceClient

router = APIRouter()
 

# Добавление участника в команду
@router.post("/teams/{team_id}/members/", response_model=schemas.TeamMemberRead)
async def add_team_member(team_id: int, member: schemas.TeamMemberCreate):
    await UserServiceClient.check_user_exists(member.user_id)
    member.team_id = team_id  # Устанавливаем ID команды
    member_obj = await TeamMemberRepository.add_member(member)
    return schemas.TeamMemberRead.from_orm(member_obj)

# Получение участников команды
@router.get("/teams/{team_id}/members/", response_model=list[schemas.TeamMemberRead])
async def get_team_members(team_id: int):
    members = await TeamMemberRepository.get_members_by_team(team_id)
    return [schemas.TeamMemberRead.from_orm(member) for member in members]

# Маршруты для команд
@router.post("/teams/", response_model=schemas.TeamRead)
async def create_team(team: schemas.TeamCreate):
    team_obj = await repositories.TeamRepository.create_team(team)
    return schemas.TeamRead.from_orm(team_obj)

@router.get("/teams/{team_id}", response_model=schemas.TeamRead)
async def get_team(team_id: int):
    # Получаем команду
    team = await repositories.TeamRepository.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")

    # Извлекаем участников команды
    members = await repositories.TeamMemberRepository.get_members_by_team(team_id)

    # Преобразуем команду в схему Pydantic
    team_data = schemas.TeamRead(
        id=team.id,
        name=team.name,
        captain_id=team.captain_id,
        created_at=team.created_at,
        members=[schemas.TeamMemberRead.from_orm(member) for member in members]
    )
    return team_data

# Маршруты для регистраций
@router.post("/registrations/", response_model=schemas.RegistrationRead)
async def create_registration(registration: schemas.RegistrationCreate):
    # Проверяем существование турнира
    await TournamentServiceClient.check_tournament_exists(registration.tournament_id)

    # Создаем регистрацию
    registration_obj = await repositories.RegistrationRepository.create_registration(registration)
    return schemas.RegistrationRead.from_orm(registration_obj)
