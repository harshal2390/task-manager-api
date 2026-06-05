from fastapi import APIRouter,Depends,HTTPException,status

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.dependencies import (get_db,get_current_user)

from app.models.user import User

from app.schemas.user import (UserCreate,UserResponse)

from app.schemas.auth import Token

from app.services.auth_service import (create_user,authenticate_user)

from app.core.security import create_access_token


router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate,db: Session = Depends(get_db)):
    return create_user(db=db,user_data=user_data)


@router.post("/token",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user(db=db,email=form_data.username,password=form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token,"token_type": "bearer"}


@router.get("/me",response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user