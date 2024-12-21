import aio_pika
from app.schemas import UserCreatedMessage
from app.emailer import send_email
from app.config import settings

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
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

async def start_consumer():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("user_created_queue", durable=True)

    await queue.consume(process_message)
    print("Консьюмер запущен и ожидает сообщений")
