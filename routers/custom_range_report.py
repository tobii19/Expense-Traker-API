from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from models.transaction import Transaction
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

router = APIRouter(
    prefix="/custom_report",
    tags=['Custom Report Range']
)

@router.get("/custom_range")
def custom_report(start_date : date,end_date : date,db : Session = Depends(get_db)):
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == 'income',
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).scalar() or 0
    
    
    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == 'expense',
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).scalar() or 0
    
    return {
        "start_Date" : start_date,
        "End Date" : end_date,
        "Income" : income,
        "Expense" : expense,
        "Balance" : income - expense
    }
    
