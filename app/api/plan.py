from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.crud.plans import create_new_plan

router = APIRouter(prefix="/plan", tags=["Plans"])


@router.post("/new")
def create_new_user_plan(
    plan_type: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_plan = create_new_plan(plan_type, 3, current_user.id, db)
    return new_plan
