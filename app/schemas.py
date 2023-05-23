
from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional



class post1(BaseModel):
    title:str
    content:str
    published: bool= True
    

class Postcreate(post1):
    pass   



class cruser(BaseModel):
     email:EmailStr
     password:str


class userout(BaseModel):
     email:EmailStr
     id:int
     class Config:
        orm_mode=True
class respoclass(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime
    owner_id:int
    owner:userout

   # owner_id:int

    class Config:
        orm_mode=True        
          

class Userlogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class Token_data(BaseModel):
    id:Optional[str] =None       
class Vote(BaseModel):
    post_id:int
    dirn:conint(le=1)

class Post_Out(BaseModel):
    Post:respoclass
    votes:int
    class Config:
        orm_mode=True

  




   