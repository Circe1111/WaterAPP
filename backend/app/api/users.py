from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.utils.database import get_db
from app.models import User

router = APIRouter()


def get_current_user_id():
    return 1


class GoalRequest(BaseModel):
    goal: int


@router.get("/goal")
def get_goal(db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return {"goal": user.daily_goal}
    return {"goal": 2000}


@router.put("/goal")
def set_goal(req: GoalRequest, db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.daily_goal = req.goal
        db.commit()
        return {"message": "updated", "goal": req.goal}
    return {"message": "user not found"}
