from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.api import router
from app.config import settings

app = FastAPI(title="Tournament Service")

# Подключение роутов
app.include_router(router)

# Регистрация Tortoise ORM
register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
