from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import auth, records, friends, reminders, users
from app.utils.database import engine
from app.models.base import Base

app = FastAPI(title="WaterAPP API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(records.router, prefix="/api/records", tags=["records"])
app.include_router(friends.router, prefix="/api/friends", tags=["friends"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "WaterAPP API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
