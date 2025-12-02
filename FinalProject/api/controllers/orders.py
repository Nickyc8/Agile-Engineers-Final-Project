from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import random
import string
from ..models.orders import Order
from ..models.promotions import Promotion

ALLOWED_STATUSES = ["Pending", "Preparing", "Ready", "Completed", "Cancelled"]


def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def create(db: Session, request):
    status_value = request.order_status or "Pending"
    if status_value not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid order status")

    promo = None
    if request.promotion_id:
        promo = db.query(Promotion).filter(Promotion.id == request.promotion_id).first()
        if not promo:
            raise HTTPException(status_code=404, detail="Promotion ID not found")
        if promo.expiration_date < datetime.now():
            raise HTTPException(status_code=400, detail="Promotion has expired")

    tracking_number = generate_tracking_number()

    new_item = Order(
        customer_id=request.customer_id,
        description=request.description,
        order_status=status_value,
        promotion_id=request.promotion_id,
        tracking_number=tracking_number,
        total_price=0
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)

    return new_item


def read_all(db: Session):
    try:
        return db.query(Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)


def read_one(db: Session, item_id: int):
    try:
        item = db.query(Order).filter(Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Id not found!")
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)


def update(db: Session, item_id: int, request):
    try:
        item = db.query(Order).filter(Order.id == item_id)
        current = item.first()

        if not current:
            raise HTTPException(status_code=404, detail="Id not found!")

        if request.order_status and request.order_status not in ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid order status")

        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()

        return item.first()

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)


def delete(db: Session, item_id: int):
    try:
        item = db.query(Order).filter(Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=404, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)
