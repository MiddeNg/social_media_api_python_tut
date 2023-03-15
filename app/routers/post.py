from statistics import mode
from fastapi import Response, status, HTTPException,Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

from .. import model, schema, oath2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schema.PostResponseVote])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()

    results = db.query(model.Post, func.count(model.Vote.post_id).label("Votes")).join(model.Vote, model.Vote.post_id==model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.owner_id == current_user.id, model.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_posts(post: schema.PostCreate, 
                 db: Session = Depends(get_db),
                 current_user = Depends(oath2.get_current_user)):
    #cursor.execute("""insert into posts (title, content, published) values
    #(%s, %s, %s) returning * """, (post.title, post.content, post.published))
    #
    #new_post = cursor.fetchone()
    #conn.commit()
    print(current_user.email)

    new_post = model.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schema.PostResponseVote)
def find_post(id: int, db: Session = Depends(get_db),
              current_user = Depends(oath2.get_current_user)):
    #cursor.execute("""select * from posts where id = %s""", (str(id),))
    #post = cursor.fetchone()
    results = db.query(model.Post, func.count(model.Vote.post_id).label("Votes")).join(model.Vote, model.Vote.post_id==model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if results.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")

    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                 current_user = Depends(oath2.get_current_user)):

    #cursor.execute("""delete from posts where id = %s 
    #returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    #
    post_query = db.query(model.Post).filter(model.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.PostResponse)
def update_post(id: int, updated_post: schema.PostBase, 
                db: Session = Depends(get_db),
                current_user = Depends(oath2.get_current_user)):

    #cursor.execute("""update posts set title = %s, 
    #content = %s, published = %s where id = %s
    #returning *""", (post.title, post.content, post.published, str(id)))
    #
    #updated_post = cursor.fetchone()
    #conn.commit()
    #
    post_query = db.query(model.Post).filter(model.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")

    post_query.update(updated_post.dict(),
                       synchronize_session=False)
    db.commit()
    return post_query.first()

