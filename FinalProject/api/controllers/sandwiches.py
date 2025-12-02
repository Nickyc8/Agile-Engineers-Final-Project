from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import sandwiches as model
from ..models import reviews as review_model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=400, detail=error)
    return new_item


def read_all(db: Session):
    try:
        return db.query(model.Sandwich).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=400, detail=error)


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Id not found!")
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=400, detail=error)


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=404, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=400, detail=error)


def delete(db: Session, item_id):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=404, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=400, detail=error)


def search(db: Session, keyword: str, dietary: str = None):
    try:
        query = db.query(model.Sandwich)

        if keyword:
            keyword_pattern = f"%{keyword.lower()}%"
            query = query.filter(model.Sandwich.sandwich_name.ilike(keyword_pattern))

        if dietary:
            # Search for dietary tag in the comma-separated list
            dietary_pattern = f"%{dietary.lower()}%"
            query = query.filter(model.Sandwich.dietary_tags.ilike(dietary_pattern))

        items = query.all()
        return items
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")


def popularity(db: Session):
    try:
        sandwiches = db.query(model.Sandwich).all()
        result = []

        for s in sandwiches:
            reviews = db.query(review_model.Review).filter(
                review_model.Review.sandwich_id == s.id
            ).all()

            count = len(reviews)

            if count > 0:
                avg = sum([r.score for r in reviews]) / count
            else:
                avg = 0

            result.append({
                "sandwich_id": s.id,
                "name": s.sandwich_name,
                "dietary_tags": s.dietary_tags,
                "review_count": count,
                "average_rating": avg
            })

        result.sort(key=lambda x: (-x["average_rating"], -x["review_count"]))
        return result

    except Exception:
        raise HTTPException(status_code=400, detail="Popularity calculation failed")

