from .. import model, schema, utils
from fastapi import status, HTTPException,Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oath2

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.VoteCreate, db: Session = Depends(get_db),
         current_user: int = Depends(oath2.get_current_user)):

    if (db.query(model.Post).filter(model.Post.id == vote.post_id).first() is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")

    vote_query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id)

    if(vote_query.first()):
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "deleted voted"}

    else:
        db.add(model.Vote(user_id=current_user.id, **vote.dict()))
        db.commit()
        return {"message": "voted"}

