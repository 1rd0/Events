from app.models import Tournament, Game
from app.schemas import TournamentCreate, GameCreate
from tortoise.exceptions import DoesNotExist

class TournamentRepository:
    @staticmethod
    async def create_tournament(data: TournamentCreate) -> Tournament:
        return await Tournament.create(**data.dict())

    @staticmethod
    async def get_tournament_by_id(tournament_id: int) -> Tournament:
        return await Tournament.get_or_none(id=tournament_id)

    @staticmethod
    async def get_all_tournaments() -> list[Tournament]:
        return await Tournament.all()

    @staticmethod
    async def delete_tournament(tournament_id: int) -> bool:
        tournament = await Tournament.get_or_none(id=tournament_id)
        if tournament:
            await tournament.delete()
            return True
        return False

class GameRepository:
    @staticmethod
    async def create_game(data: GameCreate) -> Game:
        return await Game.create(**data.dict())

    @staticmethod
    async def get_games_by_tournament(tournament_id: int) -> list[Game]:
        return await Game.filter(tournament_id=tournament_id)
