from datetime import datetime

from sqlalchemy.orm import Session
from app.models.plan import Plan, Plans
from app.schemas.plan import Plan as PlanSchema, UserPlan
from app.core.exceptions import BadRequest
from typing import List
from shortuuid import uuid


def get_plans(db: Session) -> List[PlanSchema]:
    plans_orm = db.query(Plan).all()
    plans = [PlanSchema.from_orm(plan) for plan in plans_orm]
    return plans


def get_plan(plan_id: int, db: Session) -> PlanSchema | None:
    plan_orm = db.query(Plan).filter_by(id=plan_id).first()
    if not plan_orm:
        return None
    return PlanSchema.from_orm(plan_orm)


def create_new_plan(
    type_id: int,
    duration: int,
    owner_id: int,
    db: Session,
):
    plan_type = get_plan(type_id, db)
    if not plan_type:
        raise BadRequest("Invalid plan id")

    curuent_date = datetime.utcnow()
    active = curuent_date.date == 1 or curuent_date.date == 2

    new_plan = Plans(
        plan_type_id=type_id,
        duration=duration,
        trxId=uuid(),
        owner_id=owner_id,  # type: ignore
        state="active" if active else "pending",
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


def get_user_plans(user_id: int, db: Session) -> List[UserPlan]:
    plans = db.query(Plans).filter_by(owner_id=user_id).all()
    plns = [UserPlan.from_orm(plan) for plan in plans]
    return plns
