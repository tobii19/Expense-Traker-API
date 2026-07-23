from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from models.transaction import Transaction
from sqlalchemy import func,asc,desc

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)
@router.get("/monthly")
def monthly_report(month : int, year : int,db : Session = Depends(get_db)):
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == 'income',
        func.extract("month",Transaction.date) == month,
        func.extract("year",Transaction.date) == year
        ).scalar() or 0
    
    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == 'expense',
        func.extract("month",Transaction.date) == month,
        func.extract("year",Transaction.date) == year
    ).scalar() or 0
    
    return {
        "month" : month,
        "year" : year,
        "income" : income,
        "expense" : expense,
        "Balance" : income - expense,
    }
    
@router.get("/pagination")
def page_transction(skip : int = 0, limit : int = 10,db : Session = Depends(get_db)):
    return {
        "Transcation" : db.query(Transaction).offset(skip).limit(limit).all()
    }
    
@router.get("/sorting")
def sort_transaction(order : str = "asc",db : Session = Depends(get_db)):
    sort = db.query(Transaction)    
    if order == "asc":
        sort = sort.order_by(asc(Transaction.amount))
    if order == "desc":
        sort = sort.order_by(desc(Transaction.amount))
        
    return sort.all()
        
        
@router.get("/transaction/search")
def search_transaction(keyword: str, db: Session = Depends(get_db)):
    keyword  = keyword.lower()
    return (
        db.query(Transaction)
        .filter(Transaction.type.ilike(f"%{keyword}%"))
        .all()
    )
