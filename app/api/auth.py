from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import CreateUser, UserResponse
from app.api.dependencies import get_db
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, Jwt

router = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/sign-up", response_model=UserResponse)
def create_new_user(
    userIn: CreateUser,
    db: Session = Depends(get_db),
):
    new_user = create_user(userIn, db)
    return new_user


@router.post("/login")
def login_user(
    request_form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(request_form.username, db)

    if not user:
        raise HTTPException(400, "Invalid credentials")

    correct_pwd = verify_password(request_form.password, user.password)
    if not correct_pwd:
        raise HTTPException(400, "Invalid credentials")

    token = Jwt.get_access_token(user.email)
    return {"access_token": token}
