from fastapi import APIRouter, HTTPException
from config.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/projects", tags=["Projects"])

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]
projects_collection = db["projects"]

@router.get("/")
async def list_projects():
    projects = []
    async for project in projects_collection.find({}, {"_id": 0}):
        projects.append(project)
    return projects

@router.post("/")
async def create_project(project: dict):
    if not project.get("title"):
        raise HTTPException(status_code=400, detail="Project title is required")
    await projects_collection.insert_one(project)
    return {"message": "Project created successfully"}

@router.put("/{title}")
async def update_project(title: str, updates: dict):
    result = await projects_collection.update_one({"title": title}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or no changes made")
    return {"message": "Project updated successfully"}

@router.delete("/{title}")
async def delete_project(title: str):
    result = await projects_collection.delete_one({"title": title})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}