from .. import models,schemas,utils
from .. database import get_db
from sqlalchemy.orm import Session
from  fastapi import Depends,HTTPException,status,APIRouter

router = APIRouter(
    prefix="/users",tags=["users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.userout)
def crusers(var:schemas.cruser,db: Session =Depends(get_db)):
    hashed_password=utils.hash(var.password)
    var.password=hashed_password
    new_user=models.User(**var.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.userout) 
def getoneuserid(id:int, db: Session =Depends(get_db)): 

     userid =  db.query(models.User).filter(models.User.id==id).first()

     if not userid:
         raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail={"msg":"no"})
     return userid
