import requests
from app.schemas.user import UserBank
from app.core.config import settings


def verify_bank(detail: UserBank) -> bool:
    print(detail)
    account_number = detail.bank_account
    bank_id = detail.bank_id

    res = requests.get(
        f"https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_id}",
        headers={"Authorization": "Bearer " + settings.PAYSTACK_KEY},
    )

    bank_resolution = res.json()
    print(bank_resolution)
    if not bank_resolution["status"]:
        return False

    input_bank_name = set(detail.account_name.lower().strip().split(" "))
    account_name = set(
        bank_resolution["data"]["account_name"].lower().strip().split(" "),
    )

    matching_names = account_name.intersection(input_bank_name)

    if len(matching_names) < 2:
        return False

    return True
