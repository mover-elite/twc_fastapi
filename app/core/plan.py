import json
from sqlalchemy.orm import Session
from app.services import cryptopayment
from app.schemas.plan import PlanPayment, PaymentStatus
from app.core.cache import redis_cache
from app.crud.plans import create_new_plan
from app.core.exceptions import NotFound, BadRequest
from app.services.cryptopayment import (
    check_usdt_balance,
    complete_payment as complete_payment_func,
)
from eth_typing import ChecksumAddress


def convert_str_to_int(id: str) -> int:
    ords = [str(ord(x)) for x in id]
    return int("".join(ords))


def create_plan_payment(
    user_id: int,
    amount: int,
    duration: int,
):
    details = cryptopayment.create_payment()
    payment = PlanPayment(
        payment_id=details.id,
        user_id=user_id,
        amount=amount,
        to_address=details.address,
        duration=duration,
    )
    data = json.dumps(payment.model_dump())
    redis_cache.set(payment.payment_id, data)
    return payment


def check_payment_status(
    payment_id: str,
) -> PaymentStatus:
    data = redis_cache.get(payment_id)

    if not data:
        raise NotFound("Payment ID not found")

    details = json.loads(str(data))
    to_address = details["to_address"]
    amount = details["amount"]
    balance = check_usdt_balance(to_address, amount * 10**18)
    payed = int(balance / 10**18)

    details["status"] = "completed" if payed >= amount else "pending"
    details["payed"] = payed
    status = PaymentStatus(**details)
    return status


def cancle_payment(
    payment_id: str,
    user_id: int,
    to: ChecksumAddress | None = None,
    create_new: bool = False,
):
    data = redis_cache.get(payment_id)
    print(data)
    if not data:
        raise BadRequest("Payment ID not found")

    details = json.loads(str(data))
    to_address = details["to_address"]
    balance = check_usdt_balance(to_address)
    payment_user_id = details["user_id"]
    amount = details["amount"]
    duration = details["duration"]

    if payment_user_id != user_id:
        raise BadRequest("Only Owner can cancle payment")

    res = True
    new_plan = None
    balance = int(balance / 10**18)

    if balance > 0:
        res = (
            complete_payment_func(payment_id, balance)
            if not to
            else complete_payment_func(payment_id, balance, to)
        )
    redis_cache.delete(payment_id)

    if create_new:
        new_plan = create_plan_payment(user_id, amount, duration)
        return new_plan

    return {"result": res, "new_plan": new_plan}


def complete_payment(payment_id: str, db: Session):
    data = redis_cache.get(payment_id)

    if not data:
        raise NotFound("Payment ID not found")

    details = json.loads(str(data))
    amount = details["amount"]
    duration = details["duration"]

    user_id = details["user_id"]
    to_address = details["to_address"]
    balance = check_usdt_balance(to_address, amount * 10**18) / 10**18

    if balance < amount:
        raise BadRequest("Payment Not Completed")

    complete_payment_func(payment_id, amount)

    new_plan = create_new_plan(
        amount,
        duration,
        user_id,
        payment_id,
        db,
    )
    redis_cache.delete(payment_id)
    return new_plan
