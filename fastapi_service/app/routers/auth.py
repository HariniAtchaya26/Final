from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.db.database import users_collection
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    existing_user = await users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = {
        "email": user.email,
        "password": hash_password(user.password)
    }

    await users_collection.insert_one(new_user)

    return {"email": user.email}


@router.post("/login")
async def login(user: UserCreate):
    db_user = await users_collection.find_one(
        {"email": user.email}
    )

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}
