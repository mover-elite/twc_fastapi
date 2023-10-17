from pydantic import BaseModel
from datetime import datetime


class Plan(BaseModel):
    id: int | None = None
    name: str
    price: float
    category: str
    trading_idea: bool
    live_support: bool
    state: str

    class Config:
        from_attributes = True


class PlanDet(BaseModel):
    price: float
    name: str


class UserPlan(BaseModel):
    id: int
    duration: int
    date_created: datetime
    start_date: datetime | None = None
    date_completed: datetime | None = None
    state: str
    trxId: str
    owner_id: int
    plan_type: Plan

    class Config:
        from_attributes = True
