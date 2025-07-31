from pydantic import BaseModel, field_validator

class UsageCreate(BaseModel):
    location: str
    year: int
    usage_percentage: float
    source: str

    class Config:
        orm_mode=True