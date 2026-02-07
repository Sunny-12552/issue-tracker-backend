from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# 🔐 LOGIN
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # 🔍 Find user by EMAIL or USERNAME
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

    # 🔑 Create JWT token
    access_token = create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# 🚪 LOGOUT
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    current_user: User = Depends(get_current_user),
):
    # ✅ JWT logout is handled on frontend
    # (token removed from localStorage)
    return None
