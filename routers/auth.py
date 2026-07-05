from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models.auth import User
from schemas.user_auth import UserLogin,UserResponse,CreateUser
from database import get_db
from auth.hashing import hashed_password,verify_password

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/register",response_model=UserResponse)
def register(user : CreateUser,db : Session = Depends(get_db)):
    
    exists = db.query(User).filter(User.email == user.email).first()
    
    if exists: 
        raise HTTPException(status_code=409,detail="User Alreay Exists")
    
    new_user = User(
        name = user.name,
        email = user.email,
        password = hashed_password(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login")
def login(user : UserLogin,db : Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=404,detail='User not Found')
    
    if not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401,detail='Invalid Password')
        
    return {
        "Login" : "Success",
    }