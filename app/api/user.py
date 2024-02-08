from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.dependencies import get_current_user, get_current_user_verified
from app.schemas.user import (
    UserResponse,
    User as UserSchema,
    PaymentDetail,
    UpdateUser,
    Wallet,
    UserWallet,
    ChangePassword,
)

from app.crud.user import add_bank_details, update_bank_details, update_user
from app.crud.plans import get_user_plans
from app.core.user import request_password_change, verify_password_change_otp
from app.core.security import hash_password

router = APIRouter(tags=["User"])


@router.get(
    "/dashboard",
    response_model=UserResponse,
    summary="Get user information",
)
def user_dashboard(
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_plans = get_user_plans(current_user.id, db)
    user = UserResponse(**current_user.dict())
    user.plans = user_plans
    return user


@router.get(
    "/payment",
    response_model=UserWallet,
    summary="Get user payment information",
)
def get_payment_details(
    current_user: UserSchema = Depends(get_current_user),
) -> PaymentDetail | PlainTextResponse:
    payment_detail = current_user.payment_detail
    return payment_detail if payment_detail else PlainTextResponse("Not set")


@router.post(
    "/payment",
    response_model=UserWallet,
    summary="Add payment detail for a user",
    description="Route to add a payment detail for user if \
        user doesn't have payment details set up already",
)
def add_payment_details(
    wallet: Wallet,
    current_user: UserSchema = Depends(get_current_user_verified),
    db: Session = Depends(get_db),
) -> PaymentDetail:
    if current_user.payment_detail:
        raise HTTPException(
            400,
            "Payment Detail already exists, use PUT to update existing detail",
        )
    new_det = add_bank_details(current_user.id, wallet.model_dump(), db)
    return new_det


@router.put(
    "/payment",
    response_model=UserWallet,
    summary="Update user payment details",
    description="""This router update user existing payment details
        Use to update both bank and wallet information.
        """,
)
def update_payment(
    new_details: Wallet,
    current_user: UserSchema = Depends(get_current_user_verified),
    db: Session = Depends(get_db),
) -> PaymentDetail | None:
    if not current_user.payment_detail:
        raise HTTPException(400, "Payment Detail not set yet")
    updated = update_bank_details(
        current_user.id,
        new_details.model_dump(),
        db,
    )
    return updated


@router.get("/update_password")
def update_password(
    current_user: UserSchema = Depends(get_current_user_verified),
):
    request_password_change(
        current_user.email,
        current_user.first_name,
        current_user.id,
    )
    return True


@router.put("/update_password")
def update_password_put(
    creds: ChangePassword,
    current_user: UserSchema = Depends(get_current_user_verified),
    db: Session = Depends(get_db),
):
    verify_password_change_otp(creds.otp, current_user.id)
    hashed_pasword = hash_password(creds.new_password)
    details = {"password": hashed_pasword}
    update_user(current_user.id, details, db)
    return True


@router.put("/user")
def update_user_info(
    detail: UpdateUser,
    current_user: UserSchema = Depends(get_current_user_verified),
    db: Session = Depends(get_db),
):
    details = detail.model_dump()
    parsed = {k: v for k, v in details.items() if v}
    if not parsed:
        raise HTTPException(
            400,
            "No detail provided, at least one field is required",
        )

    update_user(current_user.id, parsed, db)
    return True
