from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash

def seed_users(db: Session):
    users = [
        ("user1", "user1@gmail.com", "User@123"),
        ("user2", "user2@gmail.com", "User@123"),
        ("user3", "user3@gmail.com", "User@123"),
    ]

    for username, email, password in users:
        existing = db.query(User).filter(User.email == email).first()
        if not existing:
            user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash(password),
            )
            db.add(user)

    db.commit()
