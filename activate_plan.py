from datetime import datetime
from app.models.plan import Plans
from app.api.dependencies import get_db


def active_pending_plans():
    cur_date = datetime.utcnow()
    session = next(get_db())
    update = {"status": "active", "start_date": cur_date}
    session.query(Plans).filter_by(status="pending").update(update)
    session.commit()


active_pending_plans()
