from pydantic import BaseModel

class UserRegister(BaseModel):

    username: str
    password: str

class UserLogin(BaseModel):
    
    username: str
    password: str

class AdminRegister(BaseModel):
    
    username: str
    password: str

class AdminLogin(BaseModel):
    
    username: str
    password: str