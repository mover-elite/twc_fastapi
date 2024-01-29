from fastapi.exceptions import HTTPException
from pydantic import EmailStr
import json
from app.schemas.user import CreateUser, UserResponse
from sqlalchemy.orm import Session
from app.core.otp import get_code, verify_code
from app.core.email import send_verification_message, send_password_change_mail
from app.core.cache import redis_cache
from app.crud import user


def create_user(detail: CreateUser, db: Session) -> UserResponse:
    new_user = user.create_user(detail, db)
    send_verification_code(new_user.email, new_user.id)
    return new_user


def verify_email(user_id: int, otp: str, db: Session) -> bool:
    details = redis_cache.get(otp)

    if not details:
        raise HTTPException(400, "Invalid otp code")

    res = verify_code(otp)
    if not res:
        raise HTTPException(400, "Invalid otp code")

    details = json.loads(str(details))

    if details["user"] != user_id or details["for"] != "email_verification":
        raise HTTPException(400, "Invalid otp code")

    details = {"verified": True}
    user.update_user(user_id, details, db)
    redis_cache.delete(otp)
    return True


def send_verification_code(email: EmailStr, user_id: int):
    otp = get_code()
    print(otp)
    send_verification_message(email, otp)
    value = json.dumps({"user": user_id, "for": "email_verification"})
    redis_cache.set(otp, value)


def request_password_change(email: EmailStr, name: str, user_id: int):
    otp = get_code()
    send_password_change_mail(email, otp, name)
    value = json.dumps({"user": user_id, "for": "password_change"})
    redis_cache.set(otp, value)


def verify_password_change_otp(otp: str, user_id: int):
    details = redis_cache.get(otp)

    if not details:
        raise HTTPException(400, "Invalid otp code")

    res = verify_code(otp)

    if not res:
        raise HTTPException(400, "Invalid otp code")

    details = json.loads(str(details))

    if details["user"] != user_id or details["for"] != "password_change":
        raise HTTPException(400, "Invalid otp code")

    redis_cache.delete(otp)
    return True
