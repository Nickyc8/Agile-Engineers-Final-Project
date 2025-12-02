from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_details as model
from ..models import orders as order_model
from ..models import sandwiches as sandwich_model
from ..models import recipes as recipe_model
from ..models import resources as resource_model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    sandwich = db.query(sandwich_model.Sandwich).filter(
        sandwich_model.Sandwich.id == request.sandwich_id
    ).first()
    if not sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    order = db.query(order_model.Order).filter(
        order_model.Order.id == request.order_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    recipes = db.query(recipe_model.Recipe).filter(
        recipe_model.Recipe.sandwich_id == request.sandwich_id
    ).all()
    if not recipes:
        raise HTTPException(status_code=400, detail="No recipe found for this sandwich")

    for recipe_item in recipes:
        required_amount = recipe_item.amount * request.amount

        resource = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == recipe_item.resource_id
        ).first()

        if not resource:
            raise HTTPException(status_code=404, detail="Ingredient not found")

        if resource.amount < required_amount:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough {resource.item}. Required {required_amount}, available {resource.amount}"
            )

    for recipe_item in recipes:
        required_amount = recipe_item.amount * request.amount

        resource = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == recipe_item.resource_id
        ).first()

        resource.amount -= required_amount
        db.add(resource)

    new_item = model.OrderDetail(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount
    )
    db.add(new_item)

    line_price = float(sandwich.price) * request.amount
    order.total_price = float(order.total_price or 0) + line_price
    db.add(order)

    try:
        db.commit()
        db.refresh(new_item)
        db.refresh(order)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
