from fastapi import APIRouter
from app.db.database import users_collection, profiles_collection

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
async def dashboard_data():
    users = []
    profiles = []

    async for u in users_collection.find():
        u["_id"] = str(u["_id"])
        users.append(u)

    async for p in profiles_collection.find():
        p["_id"] = str(p["_id"])
        profiles.append(p)

    return {
        "users": users,
        "profiles": profiles
    }
