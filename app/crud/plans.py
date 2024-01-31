from datetime import datetime

from sqlalchemy.orm import Session
from app.models.plan import Plans
from app.schemas.plan import UserPlan
from typing import List


# def get_plans(db: Session) -> List[PlanSchema]:
#     plans_orm = db.query(Plan).all()
#     plans = [PlanSchema.from_orm(plan) for plan in plans_orm]
#     return plans


# def get_plan(plan_id: int, db: Session) -> PlanSchema | None:
#     plan_orm = db.query(Plan).filter_by(id=plan_id).first()
#     if not plan_orm:
#         return None
#     return PlanSchema.from_orm(plan_orm)


def create_new_plan(
    amount: float,
    duration: int,
    owner_id: int,
    trx_id: str,
    db: Session,
):
    curuent_date = datetime.utcnow()
    active = curuent_date.date in range(1, 6)

    new_plan = Plans(
        amount=amount,
        duration=duration,
        trx_id=trx_id,
        owner_id=owner_id,  # type: ignore
        status="active" if active else "pending",
    )
    if active:
        new_plan.start_date = curuent_date

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


def get_user_plans(user_id: int, db: Session) -> List[UserPlan]:
    plans = db.query(Plans).filter_by(owner_id=user_id).all()
    plns = [UserPlan.from_orm(plan) for plan in plans]
    return plns
