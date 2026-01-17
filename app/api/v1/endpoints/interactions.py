from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.blog import User, Post, Comment, Like
from app.schemas.blog import Comment as CommentSchema, CommentCreate, Like as LikeSchema

router = APIRouter()

@router.post("/comments", response_model=CommentSchema)
def create_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new comment on a post.
    """
    post = db.query(Post).filter(Post.id == comment_in.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        content=comment_in.content,
        post_id=comment_in.post_id,
        author_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/posts/{post_id}/comments", response_model=List[CommentSchema])
def read_comments(
    post_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve comments for a post.
    """
    return db.query(Comment).filter(Comment.post_id == post_id).all()

@router.post("/posts/{post_id}/like", response_model=LikeSchema)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Like a post.
    """
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked")
    
    db_like = Like(post_id=post_id, user_id=current_user.id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

@router.delete("/posts/{post_id}/like")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Unlike a post.
    """
    db_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()
    
    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    db.delete(db_like)
    db.commit()
    return {"message": "Unliked successfully"}
