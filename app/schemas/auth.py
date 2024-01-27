from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str


class OTP(BaseModel):
    otp: str
