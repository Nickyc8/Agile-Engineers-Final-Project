from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..models.payment_details import PaymentDetail
from ..models.orders import Order
from ..models.promotions import Promotion


def create(db: Session, request):
    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    existing_payment = db.query(PaymentDetail).filter(
        PaymentDetail.order_id == request.order_id
    ).first()
    if existing_payment:
        raise HTTPException(status_code=400, detail="Order already has a payment")

    total = float(order.total_price or 0)

    promo = None
    if order.promotion_id:
        promo = db.query(Promotion).filter(Promotion.id == order.promotion_id).first()
        if promo:
            if promo.expiration_date < datetime.now():
                raise HTTPException(status_code=400, detail="Promotion expired")

            if promo.discount_amount:
                total -= float(promo.discount_amount)

            if promo.discount_percentage:
                total -= total * (float(promo.discount_percentage) / 100)

            if total < 0:
                total = 0

    new_item = PaymentDetail(
        order_id=request.order_id,
        card_information=request.card_information,
        payment_type=request.payment_type,
        transaction_status="Paid",
        amount=total
    )

    try:
        order.order_status = "Completed"
        db.add(new_item)
        db.add(order)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)

    return new_item


def read_all(db: Session):
    try:
        return db.query(PaymentDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, item_id):
    try:
        item = db.query(PaymentDetail).filter(PaymentDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, item_id, request):
    try:
        item = db.query(PaymentDetail).filter(PaymentDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def delete(db: Session, item_id):
    try:
        item = db.query(PaymentDetail).filter(PaymentDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def revenue_by_date(db: Session, date_str: str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        payments = db.query(PaymentDetail).all()
        total = 0

        for p in payments:
            if p.payment_date.date() == date_obj:
                total += float(p.amount)

        return {"date": date_str, "revenue": total}

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format (use YYYY-MM-DD)")
