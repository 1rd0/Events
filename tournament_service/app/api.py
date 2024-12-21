from fastapi import APIRouter, HTTPException
from app.schemas import TournamentCreate, TournamentRead, GameCreate, GameRead
from app.repositories import TournamentRepository, GameRepository

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
