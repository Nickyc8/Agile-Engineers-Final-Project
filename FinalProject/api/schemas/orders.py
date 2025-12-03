from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    description: Optional[str] = None

class OrderCreate(OrderBase):
    customer_id: int
    order_status: str = "pending"
    order_type: str = "takeout"
    promotion_id: Optional[int] = None


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None
    order_type: Optional[str] = None
    total_price: Optional[Decimal] = None
    tracking_number: Optional[str] = None
    promotion_id: Optional[int] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_status: str
    total_price: Optional[Decimal] = None
    order_type: str
    tracking_number: Optional[str] = None
    customer_id: int
    promotion_id: Optional[int] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
