import aio_pika
import json
from app.schemas import TournamentRead
from typing import List
from datetime import date, datetime

def custom_json_serializer(obj):
    """
    Преобразовать объекты date и datetime в строку.
    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

async def send_tournament_update_message(tournament_obj, participants: List[int]):
    """
    Отправить сообщение об изменении турнира через RabbitMQ.
    """
    # Преобразуем данные турнира в формат JSON
    tournament_data = TournamentRead.from_orm(tournament_obj).dict()
    message = {
        "tournament": tournament_data,
        "participants": participants,
        "message": f"Tournament '{tournament_data['name']}' has been updated."
    }

    # Подключаемся к RabbitMQ
    connection = await aio_pika.connect_robust("amqp://rmuser:rmpassword@localhost:5672/")
    channel = await connection.channel()

    # Публикуем сообщение в очередь
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message, default=custom_json_serializer).encode("utf-8")),
        routing_key="tournament_change_queue",
    )
    print(f"Сообщение об обновлении турнира отправлено: {message['tournament']['name']}")
