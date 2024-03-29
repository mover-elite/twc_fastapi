import requests
from bs4 import BeautifulSoup as Soup
from fastapi import APIRouter, Request
from app.schemas.view import Article
from typing import List

router = APIRouter(tags=["Views"])


@router.get(
    "/crypto_new",
    response_model=List[Article],
    summary="Scrap news from cryptonews.com",
)
def get_crypto_new(request: Request):
    headers = {"User-Agent": request.headers.get("user-agent", "Mozilla")}
    res = requests.get("https://cryptonews.net/", headers=headers)
    html = Soup(res.content, "html.parser")
    articles_raw = html.find_all("div", class_="news-item")
    articles = []
    for ne in articles_raw:
        try:
            article = Article(
                title=ne.attrs["data-title"],
                image_link=ne.attrs["data-image"],
                link=ne.attrs["data-link"],
            )
            articles.append(article)
        except Exception:
            pass
    return articles


# @router.get(
#     "/plans",
#     response_model=List[PlanSchema],
#     summary="Rertieve all available plans",
# )
# def get_all_plans(db: Session = Depends(get_db)):
#     plans = get_plans(db)
#     return plans


# @router.get(
#     "/plan",
#     response_model=PlanSchema,
#     summary="Get a plan by it's id",
# )
# def get_plan(
#     plan_id: int,
#     db: Session = Depends(get_db),
# ) -> PlanSchema | None:
#     return get_plan_func(plan_id, db)
