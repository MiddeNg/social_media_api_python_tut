from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import get_db
from . import schema, model, utils
from . import oath2
router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
           db: Session = Depends(get_db),
           ):
    
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="wrong password or email")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="wrong password or email")
    access_token_data = {
        "user_id": user.id
        }
    access_token = oath2.create_access_token(access_token_data)
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }