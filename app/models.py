from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    original_url = Column(
        String,
        nullable=False
    )

    short_code = Column(
        String(10),
        unique=True,
        index=True, nullable=False
    )

    click_count = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    expires_at = Column(
        DateTime,
        nullable=True
    )




# =====================================================================================
# =====================================================================================