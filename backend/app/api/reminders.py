from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.utils.database import get_db
from app.models import ReminderSetting

router = APIRouter()


def get_current_user_id():
    return 1


class ReminderRequest(BaseModel):
    reminders: list[str]


@router.get("")
def get_reminders(db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    setting = db.query(ReminderSetting).filter(ReminderSetting.user_id == user_id).first()

    if not setting:
        return {"reminders": [], "enabled": False}

    return {
        "reminders": setting.times.split(",") if setting.times else [],
        "enabled": setting.enabled,
    }


@router.post("")
def save_reminders(req: ReminderRequest, db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    setting = db.query(ReminderSetting).filter(ReminderSetting.user_id == user_id).first()

    times_str = ",".join(req.reminders)

    if setting:
        setting.times = times_str
        setting.enabled = len(req.reminders) > 0
    else:
        setting = ReminderSetting(
            user_id=user_id,
            times=times_str,
            enabled=len(req.reminders) > 0,
        )
        db.add(setting)

    db.commit()
    return {"message": "saved"}
