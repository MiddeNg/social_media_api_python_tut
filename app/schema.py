from pydantic import BaseModel, conint
from datetime import datetime
from pydantic import EmailStr
from typing import Optional


#Users
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password:str


#Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    owner_info: UserResponse
    class Config:
        orm_mode = True

class PostResponseVote(BaseModel):
    Post: PostResponse
    Votes: int
    class Config:
        orm_mode = True


#token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None



#Vote
class VoteCreate(BaseModel):
    post_id: int 
