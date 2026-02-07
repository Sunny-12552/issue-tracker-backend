from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.auth import get_current_user  
from app.models.user import User
from app.models.active_session import ActiveSession
from app.models.app_settings import AppSettings

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # 🔍 Find user (email OR username)
    user = (
        db.query(User)
        .filter(
            (User.email == form_data.username) |
            (User.username == form_data.username)
        )
        .first()
    )

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # 🔐 Get app settings
    settings = db.query(AppSettings).first()
    if not settings:
        raise HTTPException(
            status_code=500,
            detail="Application settings not initialized"
        )

    # 🔍 Count active sessions
    active_count = db.query(ActiveSession).count()

    if active_count >= settings.max_active_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Maximum active users reached. Try again later."
        )

    # 🔁 Remove existing session for this user
    db.query(ActiveSession).filter(
        ActiveSession.user_id == user.id
    ).delete()

    # ➕ Create new session
    db.add(ActiveSession(user_id=user.id))
    db.commit()

    # 🔑 Create JWT token
    access_token = create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(ActiveSession).filter(
        ActiveSession.user_id == current_user.id
    ).delete()
    db.commit()
