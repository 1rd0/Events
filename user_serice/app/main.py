# app/main.py

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from app import schemas, repositories, api
from app.config import settings
 
import asyncio

app = FastAPI(
    title="Participant Service",
    description="Сервис управления участниками турниров",
    version="1.0.0"
)

# Подключение API роутов
app.include_router(api.router)

# Подключение Tortoise ORM
register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,  # В продакшене используйте миграции
    add_exception_handlers=True,
)

# Запуск Kafka Producer и Consumer при старте приложения
 
# Пример использования Producer в API роуте
from fastapi import APIRouter

router = APIRouter()

@router.post("/registrations/", response_model=schemas.RegistrationRead)
async def create_registration(registration: schemas.RegistrationCreate):
    try:
        registration_obj = await repositories.RegistrationRepository.create_registration(registration)
        # Отправка события регистрации в Kafka
        return await schemas.RegistrationRead.from_tortoise_orm(registration_obj)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
