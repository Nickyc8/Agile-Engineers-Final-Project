from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import payment_details as controller
from ..schemas import payment_details as schema

router = APIRouter(prefix="/payment-details", tags=["Payment Details"])


@router.post("/", response_model=schema.PaymentDetail)
def create(request: schema.PaymentDetailCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=list[schema.PaymentDetail])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.PaymentDetail)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.PaymentDetail)
def update(item_id: int, request: schema.PaymentDetailUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)


@router.get("/revenue/{date_str}")
def revenue(date_str: str, db: Session = Depends(get_db)):
    return controller.revenue_by_date(db, date_str)
