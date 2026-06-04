from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.user import UserCreate
from app.models.project import Project
from app.models.task import Task

from app.core.security import (hash_password,verify_password)


def create_user(db: Session,user_data: UserCreate) -> User:

    existing_user = (db.query(User).filter(User.email == user_data.email).first())

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")

    user = User(email=user_data.email,hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session,email: str,password: str):

    user = (db.query(User).filter(User.email == email).first())

    if not user:
        return None

    if not verify_password(password,user.hashed_password):
        return None

    return user