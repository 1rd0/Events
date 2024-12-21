import aio_pika

import aio_pika
from app.schemas import UserRead

async def send_user_created_message(user_obj):
    # Преобразуем ORM объект в Pydantic модель
    user_data = UserRead.from_orm(user_obj)

    # Подключаемся к RabbitMQ
    connection = await aio_pika.connect_robust("amqp://rmuser:rmpassword@localhost:5672/")
    channel = await connection.channel()

    # Публикуем сообщение
    await channel.default_exchange.publish(
        aio_pika.Message(body=user_data.json().encode("utf-8")),  # Используем метод json() Pydantic
        routing_key="user_created_queue",
    )
    print(f"Сообщение отправлено для {user_data.email}")
