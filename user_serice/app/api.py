# app/api.py

from fastapi import APIRouter, HTTPException
from app import schemas, repositories
 
router = APIRouter()

# Маршруты для пользователей
@router.post("/users/", response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate):
    try:
        user_obj = await repositories.UserRepository.create_user(user)
        return schemas.UserRead.from_orm(user_obj)  # Исправлено здесь
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/users/{user_id}", response_model=schemas.UserRead)
async def get_user(user_id: int):
    user = await repositories.UserRepository.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return schemas.UserRead.from_orm(user)  # И здесь

# Маршруты для команд
@router.post("/teams/", response_model=schemas.TeamRead)
async def create_team(team: schemas.TeamCreate):
    try:
        team_obj = await repositories.TeamRepository.create_team(team)
        return schemas.TeamRead.from_orm(team_obj)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/teams/{team_id}", response_model=schemas.TeamRead)
async def get_team(team_id: int):
    team = await repositories.TeamRepository.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    return await schemas.TeamRead.from_tortoise_orm(team)

# Маршруты для регистраций
@router.post("/registrations/", response_model=schemas.RegistrationRead)
async def create_registration(registration: schemas.RegistrationCreate):
    try:
        registration_obj = await repositories.RegistrationRepository.create_registration(registration)
        # Отправка события регистрации в Kafka
        return schemas.RegistrationRead.from_orm(registration_obj)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/registrations/{registration_id}", response_model=schemas.RegistrationRead)
async def get_registration(registration_id: int):
    registration = await repositories.RegistrationRepository.get_registration(registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Регистрация не найдена")
    return await schemas.RegistrationRead.from_tortoise_orm(registration)
