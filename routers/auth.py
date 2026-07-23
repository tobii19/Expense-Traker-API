from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models.auth import User
from schemas.user_auth import UserResponse,CreateUser
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from auth.hashing import hashed_password,verify_password
from auth.jwt_handler import create_access_token 
from auth.oauth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",response_model=UserResponse)
def register(user : CreateUser,db : Session = Depends(get_db)):
    db_user = db.query(User).filter(user.email == User.email).first()
    
    if db_user:
        raise HTTPException(status_code=404,detail="User Already Exists")
    
    new_user = User(
        name = user.name,
        email = user.email,
        password = hashed_password(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }
    
@router.post("/login")
def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user:
        raise HTTPException(status_code=404,detail="User Not Found")

    if not verify_password(form_data.password,db_user.password):
        raise HTTPException(status_code=404,detail="Invalid Password")
    
    token = create_access_token(
        {
            "sub":db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
 