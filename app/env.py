import os
import dotenv

dotenv.load_dotenv()


class ENV:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")