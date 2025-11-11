from fastapi import APIRouter, HTTPException, Depends
from config.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/profiles", tags=["Profiles"])

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]
users_collection = db["users"]

@router.get("/{email}")
async def get_profile(email: str):
    user = await users_collection.find_one({"email": email}, {"_id": 0, "password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{email}")
async def update_profile(email: str, payload: dict):
    result = await users_collection.update_one({"email": email}, {"$set": payload})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    return {"message": "Profile updated successfully"}