from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.utils.database import get_db
from app.models import User, Friendship, FriendshipStatus, WaterRecord

router = APIRouter()


def get_current_user_id():
    return 1


class FriendRequest(BaseModel):
    friend_id: int


@router.get("")
def get_friends(db: Session = Depends(get_db)):
    user_id = get_current_user_id()

    friends = (
        db.query(User, Friendship)
        .join(Friendship, (Friendship.friend_id == User.id))
        .filter(
            Friendship.user_id == user_id,
            Friendship.status == FriendshipStatus.ACCEPTED,
        )
        .all()
    )

    requests = (
        db.query(Friendship, User)
        .join(User, User.id == Friendship.user_id)
        .filter(
            Friendship.friend_id == user_id,
            Friendship.status == FriendshipStatus.PENDING,
        )
        .all()
    )

    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1)

    friend_list = []
    for user, friendship in friends:
        today_amount = (
            db.query(func.sum(WaterRecord.amount))
            .filter(
                WaterRecord.user_id == user.id,
                WaterRecord.created_at >= start,
                WaterRecord.created_at < end,
            )
            .scalar()
        ) or 0
        friend_list.append({
            "id": user.id,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "today_amount": today_amount,
        })

    request_list = []
    for friendship, user in requests:
        request_list.append({
            "id": friendship.id,
            "user": {
                "id": user.id,
                "nickname": user.nickname,
                "avatar": user.avatar,
            },
        })

    return {"friends": friend_list, "requests": request_list}


@router.get("/search")
def search_user(keyword: str = "", db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    users = (
        db.query(User)
        .filter(User.nickname.contains(keyword), User.id != user_id)
        .limit(20)
        .all()
    )
    return {
        "users": [
            {"id": u.id, "nickname": u.nickname, "avatar": u.avatar} for u in users
        ]
    }


@router.post("/request")
def send_friend_request(req: FriendRequest, db: Session = Depends(get_db)):
    user_id = get_current_user_id()

    existing = (
        db.query(Friendship)
        .filter(
            (
                (Friendship.user_id == user_id)
                & (Friendship.friend_id == req.friend_id)
            )
            | (
                (Friendship.user_id == req.friend_id)
                & (Friendship.friend_id == user_id)
            )
        )
        .first()
    )

    if existing:
        return {"message": "already_exists"}

    friendship = Friendship(user_id=user_id, friend_id=req.friend_id)
    db.add(friendship)
    db.commit()
    return {"message": "request_sent"}


@router.put("/accept/{request_id}")
def accept_friend(request_id: int, db: Session = Depends(get_db)):
    friendship = db.query(Friendship).filter(Friendship.id == request_id).first()
    if friendship:
        friendship.status = FriendshipStatus.ACCEPTED
        db.commit()
        return {"message": "accepted"}
    return {"message": "not_found"}


@router.get("/{friend_id}/records")
def get_friend_records(friend_id: int, db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1)

    records = (
        db.query(WaterRecord)
        .filter(
            WaterRecord.user_id == friend_id,
            WaterRecord.created_at >= start,
            WaterRecord.created_at < end,
        )
        .order_by(WaterRecord.created_at.desc())
        .all()
    )

    total = sum(r.amount for r in records)

    return {
        "total": total,
        "records": [
            {"id": r.id, "amount": r.amount, "created_at": r.created_at.strftime("%H:%M")}
            for r in records
        ],
    }


@router.get("/ranking")
def get_ranking(
    period: str = Query("day"),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id()
    now = datetime.utcnow()

    if period == "day":
        start = datetime(now.year, now.month, now.day)
    elif period == "week":
        start = now - timedelta(days=7)
    elif period == "month":
        start = now - timedelta(days=30)
    else:
        start = now - timedelta(days=1)

    end = now

    friend_ids = (
        db.query(Friendship.friend_id)
        .filter(
            Friendship.user_id == user_id,
            Friendship.status == FriendshipStatus.ACCEPTED,
        )
        .all()
    )
    friend_ids = [f[0] for f in friend_ids]

    rankings = (
        db.query(
            WaterRecord.user_id,
            func.sum(WaterRecord.amount).label("total"),
        )
        .filter(
            WaterRecord.user_id.in_([user_id] + friend_ids),
            WaterRecord.created_at >= start,
            WaterRecord.created_at < end,
        )
        .group_by(WaterRecord.user_id)
        .order_by(func.sum(WaterRecord.amount).desc())
        .limit(50)
        .all()
    )

    result = []
    for uid, total in rankings:
        user = db.query(User).filter(User.id == uid).first()
        result.append({
            "id": uid,
            "nickname": user.nickname if user else "未知",
            "avatar": user.avatar if user else "",
            "total": total or 0,
        })

    return {"rankings": result}
