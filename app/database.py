from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.env import ENV



if ENV.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        ENV.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(ENV.DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Models import
import app.models

# ✅ Create all tables in DB
Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# =====================================================================================
# =====================================================================================