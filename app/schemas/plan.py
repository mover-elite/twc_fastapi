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
    id: str
    amount: float
    duration: int
    date_created: datetime
    start_date: datetime | None = None
    date_completed: datetime | None = None
    status: str
    trx_id: str
    owner_id: int

    class Config:
        from_attributes = True


class PlanPayment(BaseModel):
    payment_id: str
    user_id: int
    amount: int
    to_address: str
    duration: int
    network: str = "Binance Smart Chain"
    asset: str = "USDT"


class PaymentStatus(PlanPayment):
    status: str
    payed: float


class PaymentIn(BaseModel):
    id: str
