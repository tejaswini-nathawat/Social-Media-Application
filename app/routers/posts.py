from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,oauth2
from typing import List,Optional
from sqlalchemy import  func


router=APIRouter(
    prefix="/posts"
    ,tags=["post"]

)

@router.get("/",response_model=List[schemas.Post_Out])
async def get_postsdata(db : Session = Depends(get_db),user_cur:int=Depends(oauth2.get_current_user),Limit:int =3,skip:int=0,
search:Optional[str]=""):
  #  posts= db.query(models.Post).filter(models.Post.owner_id==user_cur.id).all()
    # cur.execute("""SELEcT * FROM posts""")
    # posts=cur.fetchall()
    print(Limit)
    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip)
    
    print(results)
    return  results.all()
   # return {"message":my_posts}6


# @router.get("/posts/latest")
# def glatest():
#     pt=my_posts[len(my_posts)-1]
#     return{"details":pt}    

@router.get("/{id}", response_model=schemas.Post_Out) 
def getoneid(id:int, db: Session =Depends(get_db),user_cur:int=Depends(oauth2.get_current_user)):
#de getoneid(id:int, res:Response):
   # print(id)
    
    #postprint=find_posts(id)

    # cur.execute("""SELECT * FROM posts where id=%s""",(str(id)))
    # p=cur.fetchone()
    #p = db.query(models.Post).filter(models.Post.id==id).first()
    p = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # if not postprint :
      #  raise HTTPException(    status_code     =    status.HTTP_404_NOT_FOUND  ,    detail   =    {"msg":"no"})
        
       # res.status_code=status.HTTP_205_RESET_CONTENT 
        #return {"message":f"it was not found{id}"}
  

    #return {"detail in post":f"here is the post       {postprint}"}
    if not p :
     raise HTTPException(    status_code     =    status.HTTP_404_NOT_FOUND  ,    detail   =    {"msg":"no"})
        
   # if p.owner_id   != user_cur.id  :  
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user not authorised to perform this action")

    return p

# @router.post("/createposts")
# def crposts(var: post1):
#     dict= var.dict()
#     dict["id"]=randrange(0,1000000)
#     my_posts.routerend(dict)
#     print(var.dict())
#     return {"message":dict}  

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.respoclass,)
def crposts(var:schemas.Postcreate,db: Session =Depends(get_db),user_cur:int=Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,(var.title,var.content,var.published))
    # new_post=cur.fetchone()
    # conn.commit()
    # p=models.Post(title=var.title,content=var.content,published=var.published)

    print(user_cur)
    p=models.Post(owner_id=user_cur.id,**var.dict())

    db.add(p)
    db.commit()
    db.refresh(p)

    return  p

# delete post using the data from the database 

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db : Session = Depends(get_db),user_cur:int=Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE  FROM posts where id = %s returning *""", (str(id)))
    # deletedpost=cur.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id==id)
    
    if post_query.first()==None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,detail="record not found")
    if post_query.first().owner_id   != user_cur.id  :  
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user not authorised to perform this action")   
    post_query.delete(synchronize_session=False)
    db.commit()
    # db.refresh()    


# updated post using postgres database 

@router.put("/{id}",response_model=schemas.respoclass)
def update_post(id:int,var:schemas.post1,db: Session=Depends(get_db),user_cur:int=Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id = %s returning *;""",(var.title,var.content,var.published,str(id)))
    # uppost=cur.fetchone()
    # conn.commit()


   k= db.query(models.Post).filter(models.Post.id==id)
   ok=k.first()
   if ok==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id to be updated does not exist")
#    k.update({'title':'spotify', 'content':'hwihidhwik','published':'true'})
   if ok.owner_id != user_cur.id  :  
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user not authorised, to perform this action")

   k.update(var.dict(),synchronize_session=False)
   db.commit()   
   return k.first()    


