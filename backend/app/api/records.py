from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.utils.database import get_db
from app.models import WaterRecord

router = APIRouter()


class RecordRequest(BaseModel):
    amount: int


# Mock user_id, 实际项目从 JWT token 中获取
def get_current_user_id():
    return 1


@router.get("/today")
def get_today_records(db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1)

    records = (
        db.query(WaterRecord)
        .filter(
            WaterRecord.user_id == user_id,
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
            {
                "id": r.id,
                "amount": r.amount,
                "created_at": r.created_at.strftime("%H:%M"),
            }
            for r in records
        ],
    }


@router.post("")
def add_record(req: RecordRequest, db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    record = WaterRecord(user_id=user_id, amount=req.amount)
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "amount": record.amount,
        "created_at": record.created_at.strftime("%Y-%m-%d %H:%M"),
    }


@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    record = (
        db.query(WaterRecord)
        .filter(WaterRecord.id == record_id, WaterRecord.user_id == user_id)
        .first()
    )
    if record:
        db.delete(record)
        db.commit()
        return {"message": "deleted"}
    return {"message": "not found"}


@router.get("")
def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id()
    offset = (page - 1) * page_size

    records = (
        db.query(WaterRecord)
        .filter(WaterRecord.user_id == user_id)
        .order_by(WaterRecord.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    # Group by date
    grouped = {}
    for r in records:
        date_key = r.created_at.strftime("%Y-%m-%d")
        if date_key not in grouped:
            grouped[date_key] = {"date": date_key, "total": 0, "details": []}
        grouped[date_key]["total"] += r.amount
        grouped[date_key]["details"].append(
            {
                "id": r.id,
                "amount": r.amount,
                "created_at": r.created_at.strftime("%H:%M"),
            }
        )

    return {"records": list(grouped.values())}


@router.get("/stats")
def get_stats(
    period: str = Query("week"),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id()
    now = datetime.utcnow()

    if period == "week":
        days = 7
    elif period == "month":
        days = 30
    else:
        days = 7

    start = now - timedelta(days=days)

    records = (
        db.query(WaterRecord)
        .filter(
            WaterRecord.user_id == user_id,
            WaterRecord.created_at >= start,
        )
        .all()
    )

    daily_totals = {}
    for r in records:
        date_key = r.created_at.strftime("%m-%d")
        daily_totals[date_key] = daily_totals.get(date_key, 0) + r.amount

    total = sum(daily_totals.values())
    day_count = len(daily_totals) or 1
    avg = total // day_count
    max_amount = max(daily_totals.values()) if daily_totals else 0

    goal = 2000
    days_on_target = sum(1 for v in daily_totals.values() if v >= goal)

    chart_data = [
        {"label": date, "amount": amount}
        for date, amount in sorted(daily_totals.items())
    ]

    return {
        "stats": {
            "total": total,
            "avg": avg,
            "max": max_amount,
            "days": days_on_target,
        },
        "chart_data": chart_data,
    }
