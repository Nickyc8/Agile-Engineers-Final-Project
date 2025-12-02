from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    customer_id: int
    sandwich_id: int
    score: int
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    score: Optional[int] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    review_date: datetime

    class Config:
        orm_mode = True
