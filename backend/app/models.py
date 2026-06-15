from sqlalchemy import Column, Integer, Float, Index
from .database import Base

class HeartDisease(Base):
    __tablename__ = "heart_disease"
    __table_args__ = (
        Index("ix_heart_disease_target", "target"),
        Index("ix_heart_disease_age", "age"),
    )

    id       = Column(Integer, primary_key=True, autoincrement=True)
    age      = Column(Integer, nullable=False)
    sex      = Column(Integer, nullable=False)
    cp       = Column(Integer, nullable=False)
    trestbps = Column(Integer, nullable=True)
    chol     = Column(Integer, nullable=True)
    fbs      = Column(Integer, nullable=True)
    restecg  = Column(Integer, nullable=True)
    thalach  = Column(Integer, nullable=True)
    exang    = Column(Integer, nullable=True)
    oldpeak  = Column(Float,   nullable=True)
    slope    = Column(Integer, nullable=True)
    ca       = Column(Float,   nullable=True)
    thal     = Column(Float,   nullable=True)
    target   = Column(Integer, nullable=False)
