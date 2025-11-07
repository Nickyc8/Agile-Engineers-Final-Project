from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ReviewBase(BaseModel):
    customer_id: int
    score: int
    review_text: Optional[str] = None
    review_date: Optional[datetime] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    customer_id: Optional[int] = None
    score: Optional[int] = None
    review_text: Optional[str] = None
    review_date: Optional[datetime] = None

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True