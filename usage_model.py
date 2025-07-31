from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Float
from database import Base

class Usage(Base):
    __tablename__ = 'usages'

    id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    usage_percentage = Column(Float, nullable=False)
    source = Column(String, nullable=False)