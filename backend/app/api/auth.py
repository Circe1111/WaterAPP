from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.utils.database import get_db
from app.models import User

router = APIRouter()


class LoginRequest(BaseModel):
    code: str


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    # 实际项目需要调用 wx.login() 获取的 code 换取 openid
    # 此处简化为使用 code 作为模拟 openid
    mock_openid = f"wx_{req.code}"

    user = db.query(User).filter(User.openid == mock_openid).first()
    if not user:
        user = User(openid=mock_openid, nickname="新用户")
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "user_id": user.id,
        "openid": user.openid,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "daily_goal": user.daily_goal
    }
