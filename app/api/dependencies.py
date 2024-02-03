from fastapi import Depends, Security, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from fastapi.exceptions import HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.auth import RefreshToken
from app.schemas.user import User as UserSchema
from app.core.security import Jwt
from app.crud.user import get_user_by_email

security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        print("closed")
        db.close()


def decode_refresh_token(auth: RefreshToken):
    payload = Jwt.decode_refresh_token(auth.refresh_token)
    return payload["sub"]


def decode_access_token(
    auth: HTTPAuthorizationCredentials = Security(security),
):
    payload = Jwt.decode_access_token(auth.credentials)
    return payload["sub"]


# def get_current_user(
#     subject: str = Depends(decode_access_token),
#     db: Session = Depends(get_db),
# ) -> UserSchema:
#     current_user = get_user_by_email(subject, db)
#     if not current_user:
#         raise Unauthenticated("user is not authenticated")
#     return UserSchema.from_orm(current_user)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = Jwt.decode_access_token(token)

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    current_user = get_user_by_email(email, db)
    if current_user is None:
        raise credentials_exception
    return current_user
