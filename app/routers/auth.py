from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm=Depends() ,db: Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email==user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid cred")

    if not utils.verify(user.password,db_user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credientials")

    


# create a token 
# return token
    access_token=oauth2.gen_token(data={"user_id": db_user.id})
    return{"access_token":access_token,"token_type":"bearer"}
    
 