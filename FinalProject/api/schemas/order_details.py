from pydantic import BaseModel
from typing import Optional


class OrderDetailBase(BaseModel):
    order_id: int
    sandwich_id: int
    amount: int


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int

    class Config:
        orm_mode = True
