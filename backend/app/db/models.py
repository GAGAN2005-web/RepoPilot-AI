from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)

    owner = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(500), unique=True, nullable=False)

    description = Column(Text, nullable=True)
    language = Column(String(100), nullable=True)

    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)

    default_branch = Column(String(255), nullable=False)

    indexing_status = Column(
        String(50),
        default="pending",
        nullable=False,
    )