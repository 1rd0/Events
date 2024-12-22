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
    # Создаем команду
    team_obj = await repositories.TeamRepository.create_team(team)

    # Преобразуем в объект Pydantic, с пустым списком участников
    return schemas.TeamRead(
        id=team_obj.id,
        name=team_obj.name,
        captain_id=team_obj.captain_id,
        created_at=team_obj.created_at,
        members=[]  # Пустой список участников, т.к. команда только что создана
    )


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
@router.get("/registrations/by-tournament/{tournament_id}", response_model=list[schemas.TeamRead])
async def get_teams_by_tournament(tournament_id: int):
    """
    Получить список команд, зарегистрированных в указанном турнире.
    """
    # Получаем все регистрации для турнира
    registrations = await repositories.RegistrationRepository.get_registrations_by_tournament(tournament_id)
    
    if not registrations:
        raise HTTPException(status_code=404, detail="Нет зарегистрированных команд для этого турнира")

    # Извлекаем данные о командах
    teams = []
    for registration in registrations:
        team = await repositories.TeamRepository.get_team(registration.team_id)
        if team:
            # Преобразуем команду в Pydantic-модель
            members = await repositories.TeamMemberRepository.get_members_by_team(team.id)
            teams.append(
                schemas.TeamRead(
                    id=team.id,
                    name=team.name,
                    captain_id=team.captain_id,
                    created_at=team.created_at,
                    members=[schemas.TeamMemberRead.from_orm(member) for member in members]
                )
            )
    return teams
