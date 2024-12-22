from fastapi import APIRouter, HTTPException
from app.schemas import TournamentCreate, TournamentRead, GameCreate, GameRead,TournamentUpdate
from app.repositories import TournamentRepository, GameRepository
from app.clients import TeamServiceClient
router = APIRouter()

# CRUD для турниров
@router.post("/tournaments/", response_model=TournamentRead)
async def create_tournament(tournament: TournamentCreate):
    tournament_obj = await TournamentRepository.create_tournament(tournament)
    return TournamentRead.from_orm(tournament_obj)

@router.get("/tournaments/", response_model=list[TournamentRead])
async def get_all_tournaments():
    return [TournamentRead.from_orm(t) for t in await TournamentRepository.get_all_tournaments()]

@router.get("/tournaments/{tournament_id}", response_model=TournamentRead)
async def get_tournament(tournament_id: int):
    tournament = await TournamentRepository.get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return TournamentRead.from_orm(tournament)

@router.delete("/tournaments/{tournament_id}")
async def delete_tournament(tournament_id: int):
    success = await TournamentRepository.delete_tournament(tournament_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return {"message": "Tournament deleted successfully"}

# Эндпоинты для игр
@router.post("/games/", response_model=GameRead)
async def create_game(game: GameCreate):
    game_obj = await GameRepository.create_game(game)
    return GameRead.from_orm(game_obj)

@router.get("/tournaments/{tournament_id}/games/", response_model=list[GameRead])
async def get_games_by_tournament(tournament_id: int):
    return [GameRead.from_orm(g) for g in await GameRepository.get_games_by_tournament(tournament_id)]
from app.rabbitmq import send_tournament_update_message

@router.put("/tournaments/{tournament_id}", response_model=TournamentRead)
async def update_tournament(tournament_id: int, update_data: TournamentUpdate):
    # Обновляем данные турнира
    tournament = await TournamentRepository.update_tournament(tournament_id, update_data)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    # Получаем список зарегистрированных команд через Team Service
    teams = await TeamServiceClient.get_teams_by_tournament(tournament_id)

    # Собираем email участников для уведомления
    participants = []
    for team in teams:
        for member in team["members"]:
            participants.append(member["user_id"])  # Список ID пользователей для уведомления
    print(participants)
    # Отправляем сообщение в RabbitMQ
    await send_tournament_update_message(tournament, participants)

    return TournamentRead.from_orm(tournament)


@router.get("/tournaments/{tournament_id}/teams/")
async def get_teams_in_tournament(tournament_id: int):
    """
    Получить список команд, зарегистрированных в турнире по ID.
    """
    try:
        teams = await TeamServiceClient.get_teams_by_tournament(tournament_id)
        return {"tournament_id": tournament_id, "teams": teams}
    except HTTPException as e:
        raise e
