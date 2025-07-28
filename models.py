from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Float
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, nullable=False)
    company = Column(String, nullable=False)
    name = Column(String, nullable=False)
    engine = Column(String)
    displacement = Column(String)
    horsepower = Column(Integer)
    top_speed = Column(Integer)
    zero_sixty = Column(Float)
    price = Column(Integer)
    fuel_type = Column(String)
    seats = Column(Integer)
    torque = Column(String)