import httpx
from fastapi import HTTPException

class TeamServiceClient:
    BASE_URL = "http://localhost:8001"  # Замените на адрес Team Service

    @staticmethod
    async def get_teams_by_tournament(tournament_id: int):
        """
        Отправить запрос в Team Service, чтобы получить команды, зарегистрированные на турнир.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{TeamServiceClient.BASE_URL}/registrations/by-tournament/{tournament_id}")
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    raise HTTPException(status_code=404, detail="No teams found for this tournament")
                else:
                    raise HTTPException(status_code=500, detail="Error fetching teams from Team Service")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Connection error to Team Service: {exc}")
