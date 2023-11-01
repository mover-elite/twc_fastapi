import requests
from bs4 import BeautifulSoup as Soup
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request
from app.schemas.view import Article
from app.api.dependencies import get_db
from app.crud.plans import get_plans, get_plan as get_plan_func
from typing import List

from app.schemas.plan import Plan as PlanSchema

router = APIRouter(tags=["Views"])


@router.get("/crypto_new", response_model=List[Article])
def get_crypto_new(request: Request):
    print(request.headers)

    headers = {"User-Agent": request.headers.get("user-agent", "Mozilla")}
    res = requests.get("https://cryptonews.net/", headers=headers)
    html = Soup(res.content, "html.parser")
    articles_raw = html.find_all("div", class_="news-item")
    articles = [
        Article(
            title=ne.attrs["data-title"],
            image_link=ne.attrs["data-image"],
            link=ne.attrs["data-link"],
        )
        for ne in articles_raw[:3]
    ]
    return articles


@router.get("/plans")
def get_all_plans(db: Session = Depends(get_db)):
    plans = get_plans(db)
    return plans


@router.get("/plan")
def get_plan(plan_id: int, db: Session = Depends(get_db)) -> PlanSchema | None:
    return get_plan_func(plan_id, db)



from crud.user import (
    check_user_exists,
    get_user_by_ref_code,
    check_user_by_phone,
)


@views.route("/check_user")
def get_user():
    email, ref_code, phone = [x.strip() for x in request.args.values()]
    user_exist = check_user_exists(email)
    user_exist_phone = check_user_by_phone(phone)
    correct_code = True if (not ref_code or get_user_by_ref_code(ref_code)) else False
    data = {
        "user_exist": user_exist,
        "phone_exist": user_exist_phone,
        "correct_code": correct_code,
    }
    return data
