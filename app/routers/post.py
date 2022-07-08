from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models,schemas, oauth2
from .. database import get_db
from typing import  List, Optional

router = APIRouter(
    prefix='/posts',
    tags = ['Posts']
)


#@router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)


    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter =True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post : schemas.PostCreate, db: Session = Depends(get_db), 
current_user : int = Depends(oauth2.getCurrentUser)):
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #(post.title, post.content, post.published))

    #newPost = cursor.fetchone()

    #conn.commit()

    newPost = models.Post(owner_id =current_user.id,**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost



@router.get('/{id}', response_model=schemas.PostOut)
def getPost(id: int, db: Session = Depends(get_db), currentUser : int = Depends(oauth2.getCurrentUser)):
    print(id)

    #post = findPost(id)
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()
    #print(post)
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter =True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id : int, db: Session = Depends(get_db), currentUser : int = Depends(oauth2.getCurrentUser)):
    #delete post
    # find the index in the array that has required ID
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deletedPost = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    
    if post.owner_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def updatePost(id: int, updated_post : schemas.PostCreate,  db: Session = Depends(get_db)
, currentUser : int = Depends(oauth2.getCurrentUser)):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title,post.content,post.published, str(id)),)
    #updatedPost = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
