from fastapi import APIRouter, HTTPException, Depends
from models.user import UserCreate, UserLogin
from utils.password_utils import hash_password, verify_password
from utils.jwt_handler import create_access_token
from config.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/auth", tags=["Auth"])

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]
users_collection = db["users"]

@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    await users_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}