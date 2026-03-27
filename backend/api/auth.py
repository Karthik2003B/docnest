from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register_user(user.name, user.email, user.password)


@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_user(user.email, user.password)