from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    is_active: bool

class UserUpdate(BaseModel):
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class BlogCreate(BaseModel):
    title: str
    content: str

class BlogUpdate(BaseModel):
    title: str
    content: str

class BlogOwner(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
    )
    
class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    owner: BlogOwner

    model_config = ConfigDict(
        from_attributes=True,
    )

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentUser(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class CommentResponse(BaseModel):
    id: int
    content: str
    user: CommentUser

    model_config = ConfigDict(
        from_attributes=True,
    )