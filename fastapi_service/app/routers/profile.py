from fastapi import APIRouter, HTTPException
from app.schemas.profile import Profile
from app.db.database import profiles_collection

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/")
async def create_profile(profile: Profile):
    await profiles_collection.insert_one(profile.dict())
    return {"message": "Profile created successfully"}


@router.get("/")
async def get_profiles():
    profiles = []
    async for p in profiles_collection.find():
        p["_id"] = str(p["_id"])  # Mongo fix
        profiles.append(p)

    return profiles
