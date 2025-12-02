from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema

router = APIRouter(prefix="/sandwiches", tags=["Sandwiches"])


@router.post("/", response_model=schema.Sandwich)
def create(request: schema.SandwichCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=list[schema.Sandwich])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/search/{keyword}")
def search(keyword: str, db: Session = Depends(get_db)):
    return controller.search(db, keyword)


@router.get("/popularity")
def popularity(db: Session = Depends(get_db)):
    return controller.popularity(db)


@router.get("/{item_id}", response_model=schema.Sandwich)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.Sandwich)
def update(item_id: int, request: schema.SandwichUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)
