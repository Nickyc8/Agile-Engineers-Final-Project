from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaymentDetailBase(BaseModel):
    order_id: int
    card_information: str
    payment_type: str


class PaymentDetailCreate(PaymentDetailBase):
    pass


class PaymentDetailUpdate(BaseModel):
    card_information: Optional[str] = None
    payment_type: Optional[str] = None
    transaction_status: Optional[str] = None


class PaymentDetail(PaymentDetailBase):
    id: int
    amount: float
    transaction_status: str
    payment_date: datetime

    class Config:
        orm_mode = True
