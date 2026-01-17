from pydantic import BaseModel, EmailStr, AnyHttpUrl
from typing import List, Optional
from datetime import datetime
from app.models.blog import UserRole, PostStatus

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.READER

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return via API
class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Comment Schemas
class CommentBase(BaseModel):
    content: str
    post_id: int

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    author_id: int
    created_at: datetime
    author: Optional[User] = None

    class Config:
        from_attributes = True

# Like Schemas
class LikeBase(BaseModel):
    post_id: int

class Like(LikeBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Post Schemas
class PostBase(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    read_time: Optional[str] = None
    featured: Optional[bool] = False
    status: Optional[PostStatus] = PostStatus.PUBLISHED
    category_id: Optional[int] = None

class PostCreate(PostBase):
    slug: str

class Post(PostBase):
    id: int
    slug: str
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # We can include the nested author and category objects
    author: Optional[User] = None
    category: Optional[Category] = None
    comments: List[Comment] = []
    likes_count: int = 0

    class Config:
        from_attributes = True

# Authentication Schemas
class UserLogin(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Schema for JWT token payload"""
    sub: Optional[int] = None

