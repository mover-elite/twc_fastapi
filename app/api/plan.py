from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user, get_db
from app.crud.plans import create_new_plan
from sqlalchemy.orm import Session
import shortuuid

router = APIRouter(prefix="/plan", tags=["Plan"])


@router.post("/test")
def test_new_plan(
    amount: int,
    duration: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_plan = create_new_plan(
        amount,
        duration,
        current_user.id,
        shortuuid.uuid(),
        db,
    )
    return new_plan


# @router.get(
#     "/new",
#     response_model=PlanPayment,
# )
# def create_new_user_plan(
#     amount: int,
#     duration: int,
#     current_user=Depends(get_current_user),
# ):
#     plan = create_plan_payment(current_user.id, amount, duration)
#     return plan


# @router.post("/new")
# def complete_payment(
#     payment_id: int,
# ):
#     status = check_payment_status(payment_id)
#     pass
