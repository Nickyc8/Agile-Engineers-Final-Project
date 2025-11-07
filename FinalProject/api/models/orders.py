from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    tracking_number = Column(String(50), unique=True, nullable=True)
    order_status = Column(String(50), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    customer = relationship("Customer", back_populates="orders")
    payment_detail = relationship("PaymentDetail", back_populates="order")
    promotion = relationship("Promotion", back_populates="orders")