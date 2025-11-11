from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, profiles, projects

app = FastAPI(title="SkillSync API", version="1.0.0")

origins = [
    "http://localhost:3000",
    "https://skill-sync-frontend-seven.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(projects.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
