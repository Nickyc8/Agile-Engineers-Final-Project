from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    expiration_date = Column(DATETIME, nullable=False)

    # Amount to be discounted, supports different types of discounts
    discount_percentage = Column(DECIMAL(5, 2), nullable=True)
    discount_amount = Column(DECIMAL(10, 2), nullable=True)

    orders = relationship("Order", back_populates="promotion")