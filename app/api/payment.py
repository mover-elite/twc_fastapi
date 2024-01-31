from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.core.plan import create_plan_payment, check_payment_status
from app.core.plan import complete_payment as complete_payment_func
from app.schemas.plan import PlanPayment, PaymentStatus, PaymentIn
from sqlalchemy.orm import Session
from app.api.dependencies import get_db

router = APIRouter(prefix="/payment", tags=["Payment", "Plan"])


@router.get(
    "/new",
    response_model=PlanPayment,
)
def create_new_user_plan(
    amount: int,
    duration: int,
    current_user=Depends(get_current_user),
):
    plan = create_plan_payment(current_user.id, amount, duration)
    return plan


@router.get("/status")
def check_payment_status_func(
    payment_id: str,
) -> PaymentStatus:
    status = check_payment_status(payment_id)
    return status


@router.post("/complete")
def complete_payment(
    pamyment: PaymentIn,
    db: Session = Depends(get_db),
):
    payment_id = pamyment.id
    new_plan = complete_payment_func(payment_id, db)
    return new_plan
