from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.blog import User, UserRole, Post, PostStatus
from app.schemas.blog import User as UserSchema, Post as PostSchema, PostStatus as PostStatusSchema
from app.services import user_service

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Retrieve all users. (Admin only)
    """
    return user_service.get_all_users(db)

@router.put("/users/{user_id}/role", response_model=UserSchema)
def update_user_role(
    user_id: int,
    role: UserRole,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update a user's role. (Admin only)
    """
    user = user_service.update_user_role(db, user_id=user_id, role=role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/posts/pending", response_model=List[PostSchema])
def read_pending_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Retrieve all pending posts. (Admin only)
    """
    return db.query(Post).filter(Post.status == PostStatus.PENDING).all()

@router.put("/posts/{post_id}/status", response_model=PostSchema)
def update_post_status(
    post_id: int,
    status: PostStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Approve or reject a post. (Admin only)
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.status = status
    if status == PostStatus.PUBLISHED:
        post.published = True
    elif status == PostStatus.REJECTED:
        post.published = False
        
    db.commit()
    db.refresh(post)
    return post
