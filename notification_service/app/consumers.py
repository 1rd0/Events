import aio_pika
import json
from app.schemas import UserCreatedMessage
from app.emailer import send_email

# Обработчик сообщений для очереди user_created_queue
async def process_user_created_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            # Декодируем сообщение
            data = message.body.decode("utf-8")
            user_data = UserCreatedMessage.parse_raw(data)

            # Подготовка email
            subject = "Добро пожаловать в наш сервис!"
            body = f"Здравствуйте, {user_data.full_name}!\n\nВы успешно зарегистрировались на нашем сайте."

            # Отправка email
            await send_email(user_data.email, subject, body)
            print(f"Уведомление отправлено для {user_data.email}")
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")

# Обработчик сообщений для очереди tournament_change_queue
async def process_tournament_change_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            # Декодируем сообщение
            data = message.body.decode("utf-8")
            notification_data = json.loads(data)

            # Извлекаем данные турнира и участников
            tournament = notification_data["tournament"]
            participants = notification_data["participants"]
            notification_message = notification_data["message"]
            print(participants)
            # Для каждого участника отправляем email
            for user_id in participants:
                email = await fetch_email_by_user_id(user_id)
                subject = f"Изменения в турнире {tournament['name']}"
                body = (
                    f"Здравствуйте!\n\n"
                    f"Турнир {tournament['name']} был изменён.\n"
                    f"Дата начала: {tournament['start_date']}\n"
                    f"Дата окончания: {tournament['end_date']}\n\n"
                    f"{notification_message}"
                )
                await send_email(email, subject, body)
                print(f"Уведомление отправлено для {email}")
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")

import httpx
from fastapi import HTTPException

async def fetch_email_by_user_id(user_id: int) -> str:
    """
    Получить email пользователя по user_id с использованием User Service.
    """
    BASE_URL = "http://localhost:8000"  # Адрес User Service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/users/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                return user_data["email"]
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
            else:
                raise HTTPException(status_code=500, detail="Error fetching user data")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Connection error to User Service: {e}")
# Функция запуска обоих потребителей
async def start_consumer():
    connection = await aio_pika.connect_robust("amqp://rmuser:rmpassword@localhost:5672/")
    channel = await connection.channel()

    # Настраиваем первую очередь для пользователей
    user_created_queue = await channel.declare_queue("user_created_queue", durable=True)
    await user_created_queue.consume(process_user_created_message)
    print("Слушатель для user_created_queue запущен")

    # Настраиваем вторую очередь для изменений турниров
    tournament_change_queue = await channel.declare_queue("tournament_change_queue", durable=True)
    await tournament_change_queue.consume(process_tournament_change_message)
    print("Слушатель для tournament_change_queue запущен")
