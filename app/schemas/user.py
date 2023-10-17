from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime
from typing import List
from app.schemas.plan import UserPlan

pwd_pattern = r"[A-Za-z0-9]*[A-Z]+[A-Za-z0-9]*[a-z]+[A-Za-z0-9]*\d+[A-Za-z0-9]*[^A-Za-z0-9]+[A-Za-z0-9]*"  # noqa


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBank(BaseModel):
    bank_name: str
    bank_id: str
    bank_account: str
    account_name: str

    class Config:
        from_attributes = True


class UserWallet(BaseModel):
    network: str
    wallet_address: str
    coin: str

    class Config:
        from_attributes = True


class PaymentDetailIn(BaseModel):
    bank: UserBank | None = None
    wallet: UserWallet | None = None


class PaymentDetail(UserWallet, UserBank):
    id: int

    class Config:
        from_attributes = True


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    address: str
    upline_ref_code: str | None = None


class CreateUser(BaseUser):
    password: str = Field(
        min_length=8,
        pattern=pwd_pattern,
    )


class UserResponse(BaseUser):
    id: int
    date_created: datetime
    verified: bool
    balance: float
    user_ref_code: str
    is_admin: bool
    last_login: datetime
    plans: List[UserPlan] | None = None

    class Config:
        from_attributes = True


class User(UserResponse):
    password: str = Field(
        min_length=8,
        pattern=pwd_pattern,
    )

    payment_detail: PaymentDetail | None = None

    class Config:
        from_attributes = True
