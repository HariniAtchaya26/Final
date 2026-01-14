from fastapi import FastAPI
from app.routers import auth, profile, dashboard

app = FastAPI(title="FastAPI Async Backend")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {"message": "FastAPI service running"}
