from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app import api
from app.config import settings

app = FastAPI(title="Team Service")

# Подключение API
app.include_router(api.router)

# Подключение базы данных
register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
