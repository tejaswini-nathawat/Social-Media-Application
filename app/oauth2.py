from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends, HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_TIME_MINUTES=settings.access_token_expire_minutes

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

def gen_token(data:dict ):
    to_encode=data.copy()
    expire_time= datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME_MINUTES)
    to_encode.update({"exp":expire_time})
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm =  ALGORITHM) 
    return encode_jwt

def verify_token(token:str, cred_exception): 
   
 try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        
        if not id:
            raise cred_exception 
        token_data = schemas.Token_data(id=id)
 except JWTError:
      raise cred_exception        
 return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid cred...",headers={"WWW-Authenticate":"Bearer"} )
    
    token = verify_token(token, cred_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()


   
   
   
    return user   
    