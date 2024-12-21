from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, repositories
from app.config import settings
from typing import Optional
router = APIRouter()
 

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создание и верификация токенов
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
 

# Регистрация пользователя
@router.post("/register/", response_model=schemas.UserRead)
async def register(user: schemas.UserCreate):
    user_by_email = await repositories.UserRepository.get_user_by_email(user.email)
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user_obj = await repositories.UserRepository.create_user(user)
    return schemas.UserRead.from_orm(user_obj)

# Логин и получение токена
@router.post("/login/", response_model=schemas.Token)
async def login(user: schemas.UserCreate):
    db_user = await repositories.UserRepository.get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Пример защищенного маршрута
from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Настройка для извлечения токена из заголовка Authorization
security = HTTPBearer()

# Пример защищенного маршрута
@router.get("/protected/")
async def protected_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        # Извлекаем токен из заголовков
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Недопустимый токен")
        return {"email": user_email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Недопустимый токен")

 
@router.get("/users/{user_id}", response_model=schemas.UserRead)
async def get_user(user_id: int):
    user = await repositories.UserRepository.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return schemas.UserRead.from_orm(user)  # И здесь
 