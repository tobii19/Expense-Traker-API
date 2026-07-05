from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.category import CategoryCreate, CategoryResponse
from models.categories import Category

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse)
def add_category(add: CategoryCreate, db: Session = Depends(get_db)):
    item = Category(
        name=add.name,
        type=add.type
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get("/", response_model=List[CategoryResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/{id}", response_model=CategoryResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Category).filter(Category.id == id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item Not Found")

    return db_item


@router.put("/{id}", response_model=CategoryResponse)
def update_category(
    id: int,
    update_item: CategoryCreate,
    db: Session = Depends(get_db)
):
    db_item = db.query(Category).filter(Category.id == id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item Not Found")

    db_item.name = update_item.name
    db_item.type = update_item.type

    db.commit()
    db.refresh(db_item)

    return db_item


@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Category).filter(Category.id == id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item Not Found")

    db.delete(db_item)
    db.commit()

    return {"message": "Item Deleted!"}