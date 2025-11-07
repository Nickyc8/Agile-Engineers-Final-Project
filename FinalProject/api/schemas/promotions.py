from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    code: str
    expiration_date: datetime
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    expiration_date: Optional[datetime] = None
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None

class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True