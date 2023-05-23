
from . import models
from fastapi import FastAPI
from .database import engine
from .routers import users, posts,auth,vote
from .config import settings

#print(settings.database_password)   

models.Base.metadata.create_all(bind=engine)


app=FastAPI()
app.include_router(posts.router)
app.include_router(users.router) 
app.include_router(auth.router)   
app.include_router(vote.router)      
@app.get("/")
async def root():
    return {"message":"Tejaswini Nathawat bpsr"}


















#refrences

# def find_posts(id):
#   for p in my_posts:
#     if  p["id"]== id:
#         return p

# from typing import Optional,List
# from fastapi import FastAPI, Response,status,HTTPException, Depends
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# from sqlalchemy.orm import Session
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from . import models,schemas

#my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"fav foods","content":"c2","id":"2"}]
# while True:
#     try :
#         conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='0',cursor_factory=RealDictCursor)
#         cur=conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print("database connection failed")
#         print("error",error)
#         time.sleep(3)



# neew table user registration
