from pydantic import BaseModel, Field, EmailStr, validator
from typing import List
from datetime import datetime
from app.schemas.plan import UserPlan
from eth_utils import address as eth_address
import re

pwd_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"  # noqa


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Wallet(BaseModel):
    wallet_address: str = Field(
        examples=["0xC1614F74733409B77c8dBbF512D2627823CC2c81"],
    )

    @validator("wallet_address")
    def validate_address(cls, value):
        try:
            checksumed = eth_address.to_checksum_address(value)
            return checksumed
        except Exception:
            raise ValueError("Invalid Wallet Address")


class UserWallet(BaseModel):
    network: str
    wallet_address: str
    coin: str

    class Config:
        from_attributes = True


# class PaymentDetailIn(BaseModel):
#     wallet: UserWallet


class PaymentDetail(UserWallet):
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
    password: str = Field(min_length=8)
    address: str | None = ""

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "email": "johndoe@example.com",
                "address": "123 Main St, Anytown USA",
                "upline_ref_code": "ABCD1234",
                "password": "password123",
            }
        }

    @validator("password")
    def validate_password(cls, value):
        res = re.match(pwd_pattern, value)

        if not res:
            raise ValueError("Password not strong enough")
        return value


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


class CreateUserResponse(BaseModel):
    user: UserResponse
    access_token: str


class User(UserResponse):
    password: str

    payment_detail: PaymentDetail | None = None

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=2,
        examples=["John"],
    )

    last_name: str | None = Field(
        default=None,
        min_length=2,
        examples=["Doe"],
    )

    phone_number: str | None = Field(
        default=None,
        min_length=2,
        examples=["+1234567890"],
    )
    address: str | None = Field(
        default=None,
        min_length=2,
        examples=["123 Main St, Anytown USA"],
    )


class ChangePassword(BaseModel):
    otp: str
    new_password: str = Field(min_length=8)

    @validator("new_password")
    def validate_password(cls, value):
        res = re.match(pwd_pattern, value)
        if not res:
            raise ValueError("Password not strong enough")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "otp": "123456",
                "new_password": "pAssword1@23",
            }
        }
