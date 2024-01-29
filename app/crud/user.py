from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.schemas.user import (
    CreateUser,
    UserResponse,
    User as UserSchema,
    UserWallet,
    PaymentDetail,
)
from app.models.user import User, Payment_Details
from app.core.security import hash_password
import shortuuid


def gen_ref_link():
    uuid = shortuuid.ShortUUID()
    return uuid.random(length=8)


def get_user_by_email(email: str, db: Session) -> UserSchema | None:
    user = db.query(User).filter_by(email=email).first()

    if user:
        return UserSchema.from_orm(user)
    return None


def check_user_exists(
    phone_number: str,
    email: str,
    db: Session,
) -> UserSchema | None:
    user = (
        db.query(User)
        .filter(
            or_(
                User.phone_number == phone_number,
                User.email == email,
            )
        )
        .first()
    )
    if user:
        return UserSchema.from_orm(user)
    return None


def create_user(
    new_user: CreateUser,
    db: Session,
) -> UserResponse:
    user_exists = check_user_exists(new_user.phone_number, new_user.email, db)

    if user_exists:
        msg = (
            "Phone number already in use"
            if user_exists.phone_number == new_user.phone_number
            else "Email address already in use"
        )
        raise HTTPException(400, msg)

    new_user.password = hash_password(new_user.password)
    user = User(**new_user.model_dump(), user_ref_code=gen_ref_link())
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.from_orm(user)


def add_bank_details(
    user_id: int,
    details: dict,
    db: Session,
) -> PaymentDetail:
    pay_details = Payment_Details(owner_id=user_id, **details)
    db.add(pay_details)
    db.commit()
    db.refresh(pay_details)
    return PaymentDetail.from_orm(pay_details)


def update_bank_details(
    user_id: int,
    detail: UserWallet,
    db: Session,
) -> PaymentDetail | None:
    query = db.query(Payment_Details).filter(
        Payment_Details.owner_id == user_id,
    )
    query.update(detail.model_dump())

    payment = query.first()
    if not payment:
        return None
    db.commit()
    db.refresh(payment)
    return PaymentDetail.from_orm(payment)


def update_user(user_id: int, details: dict, db: Session) -> bool:
    db.query(User).filter(User.id == user_id).update(details)
    db.commit()
    return True
