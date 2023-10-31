import pyotp

totp = pyotp.TOTP("2I6TWPXVDQ7ZURW4VQJCNUHFKDENONQA", interval=600)


def get_code() -> str:
    return totp.now()


def verify_code(otp: str) -> bool:
    return totp.verify(otp)
