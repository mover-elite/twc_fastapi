from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.dependencies import get_current_user
from app.schemas.user import (
    UserResponse,
    User as UserSchema,
    UserBank,
    PaymentDetail,
    UserWallet,
    PaymentDetailIn,
)

from app.crud.user import add_bank_details, update_bank_details
from app.crud.plans import get_user_plans
from app.core.paystack import verify_bank

router = APIRouter(tags=["User"])


@router.get("/dashboard")
def user_dashboard(
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_plans = get_user_plans(current_user.id, db)
    user = UserResponse(**current_user.dict())
    user.plans = user_plans
    return user


@router.get("/payment")
def get_payment_details(
    current_user: UserSchema = Depends(get_current_user),
) -> PaymentDetail | None:
    return current_user.payment_detail


@router.post("/payment")
def add_bank_payment_details(
    payment_details: PaymentDetailIn,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PaymentDetail:
    if current_user.payment_detail:
        raise HTTPException(
            400,
            "Payment Detail already exists, use PUT to update existing detail",
        )
    bank = payment_details.bank.dict() if payment_details.bank else {}
    if payment_details.bank:
        valid_bank = verify_bank(payment_details.bank)
        if not valid_bank:
            raise HTTPException(400, "Invalid bank details")

    wallet = payment_details.wallet.dict() if payment_details.wallet else {}
    details = {**bank, **wallet}
    if not details:
        raise HTTPException(400, "Incomplete payment details")
    new_det = add_bank_details(current_user.id, details, db)
    return new_det


@router.put("/payment")
def update_payment(
    new_details: UserBank | UserWallet,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = update_bank_details(current_user.id, new_details, db)
    return updated
