from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name : str
    email : EmailStr
    password : str
    
class UserLogin(BaseModel):
    email : str
    password : str
    
class UserResponse(BaseModel):
    id : int
    name : str
    email : EmailStr
    
    