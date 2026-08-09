from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.schemas import Token, TokenData, UserCreate, UserResponse
from backend.utils import create_access_token, get_password_hash, verify_password
from database.models import User
from database.session import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')
    access_token = create_access_token(data={'sub': user.email, 'role': user.role})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/register', response_model=UserResponse, status_code=201)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        role='citizen',
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/me', response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload or 'sub' not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication credentials')
    user = get_user_by_email(db, payload['sub'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
