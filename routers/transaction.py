from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List,Optional
from database import get_db
from models.transaction import Transaction
from models.categories import Category
from schemas.transaction import TransactionCreate,TransactionResponse
from datetime import date
from schemas.transaction_filter import TransactionFilter

router = APIRouter(
    tags = ["Transaction"]
)

@router.post("/transaction/",response_model=TransactionResponse)
def create_transaction(tran : TransactionCreate,db : Session = Depends(get_db)):
    catg = db.query(Category).filter(Category.id == tran.category_id).first()
    
    if not catg:
        raise HTTPException(status_code=404,detail="Category Not Exists")
    
    new_transaction = Transaction(
        amount = tran.amount,
        description = tran.description,
        date = tran.date,
        type = tran.type,
        category_id = tran.category_id
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction

@router.get("/transaction/",response_model=List[TransactionResponse])
def get_transaction(db : Session = Depends(get_db)):
    return db.query(Transaction).all()

@router.get("/{id}")
def get_transaction_id(id : int,db : Session =Depends(get_db)):
    tran = db.query(Transaction).filter(Transaction.id == id).first()
    
    if not tran:
        return {
            "Transaction" : "Transaction id not found"
        }
        
    return tran

@router.put("/transaction/{id}",response_model=TransactionResponse)
def update_transaction(id : int,updatetran :TransactionCreate,db : Session = Depends(get_db)):
    tran = db.query(Transaction).filter(Transaction.id == id).first()
    if not tran:
        raise HTTPException(status_code=404,detail="Transaction id not found")
    
    catg = db.query(Category).filter(Category.id == updatetran.category_id).first()
    
    if not catg:
        raise HTTPException(status_code=404,detail="Category id not found")
    
    tran.amount = updatetran.amount
    tran.description = updatetran.description
    tran.date = updatetran.date
    tran.type = updatetran.type
    tran.category_id = updatetran.category_id
    
    db.commit()
    db.refresh(tran)
    
    return tran
    
    
@router.delete("/transaction/{id}")
def delete_transaction(id : int, db : Session = Depends(get_db)):
    tran = db.query(Transaction).filter(Transaction.id == id).first()
    
    if not tran:
        raise HTTPException(status_code=404,detail="Transaction not found")
    
    db.delete(tran)
    db.commit()
    
    return {
        "Transaction" : "Delete Transaction"
    }
     
@router.get("/tsort/", response_model=List[TransactionResponse])
def sort_transactions(tsort : TransactionFilter,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if tsort.type:
        query = query.filter(Transaction.type == tsort.type)

    if tsort.category_id:
        query = query.filter(Transaction.category_id == tsort.category_id)

    if tsort.min_amount is not None:
        query = query.filter(Transaction.amount >= tsort.min_amount)

    if tsort.max_amount is not None:
        query = query.filter(Transaction.amount <= tsort.max_amount)

    if tsort.start_date:
        query = query.filter(Transaction.date >= tsort.start_date)

    if tsort.end_date:
        query = query.filter(Transaction.date <= tsort.end_date)

    return query.all()
    
    