from typing import Optional
from pydantic import BaseModel

class PaymentDetailsBase(BaseModel):
    order_id: int
    card_information: str
    transaction_status: str
    payment_type: str

class PaymentDetailsCreate(PaymentDetailsBase):
    pass

class PaymentDetailsUpdate(BaseModel):
    order_id: Optional[int] = None
    card_information: Optional[str] = None
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None

class PaymentDetails(PaymentDetailsBase):
    id: int

    class ConfigDict:
        from_attributes = True