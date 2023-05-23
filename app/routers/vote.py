from fastapi import FastAPI, Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session
from .. import oauth2, database,models,schemas


router=APIRouter(
  
  prefix="/votes",
  tags=["VOTES"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),user_curr:int=Depends(oauth2.get_current_user)):
    post_ex=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post_ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not exist")
    vote_query=db.query(models.Vote).filter(vote.post_id==models.Vote.post_id, models.Vote.user_id==user_curr.id)
    found_vote=vote_query.first()

    
    if vote.dirn==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user already voted")
        new_vote=models.Vote(post_id=vote.post_id,user_id=user_curr.id)
        db.add(new_vote)
        db.commit()
        return {"mdg":"vote raised"}
        
    else  :
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"msg":"unliked"}



        
