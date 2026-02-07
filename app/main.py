from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine, SessionLocal

# 🔥 IMPORT ALL MODELS FIRST (VERY IMPORTANT)
from app.models import (
    user,
    project,
    comment,
    active_session,
    app_settings,
)

from app.models.app_settings import AppSettings
from app.routes import users, auth, projects, comments

# 🚀 CREATE FASTAPI APP
app = FastAPI(
    title="Issue Tracker API",
    redirect_slashes=False,
)
@app.get("/")
def root():
    return {
        "message": "Issue Tracker API is running successfully 🚀",
        "docs": "/docs"
    }

# 🔐 CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 CREATE DATABASE TABLES
Base.metadata.create_all(bind=engine)

# ✅ CREATE DEFAULT APP SETTINGS (LOGIN LIMIT)
@app.on_event("startup")
def init_app_settings():
    db = SessionLocal()
    try:
        settings = db.query(AppSettings).first()
        if not settings:
            db.add(AppSettings(max_active_users=1))  # 🔒 default: 1 login at a time
            db.commit()
    finally:
        db.close()

# 🔗 REGISTER ROUTERS
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(comments.router)
