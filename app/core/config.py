import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./issue_tracker.db")

# ✅ Security
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)
