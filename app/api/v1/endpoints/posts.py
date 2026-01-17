from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.blog import Post, User, PostStatus, Like
from app.schemas.blog import Post as PostSchema, PostCreate
from app.api.deps import get_current_active_user, get_current_writer_user
from sqlalchemy import func

router = APIRouter()

@router.get("/", response_model=List[PostSchema])
def read_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    featured: Optional[bool] = None
):
    """
    Retrieve all published posts. (Public)
    """
    query = db.query(Post).filter(Post.status == PostStatus.PUBLISHED)
    
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if featured is not None:
        query = query.filter(Post.featured == featured)
        
    posts = query.offset(skip).limit(limit).all()
    
    # Add likes count (this is simplified, ideally use a hybrid property or aggregated query)
    for post in posts:
        post.likes_count = db.query(Like).filter(Like.post_id == post.id).count()
        
    return posts

@router.get("/my-posts", response_model=List[PostSchema])
def read_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve posts created by the current user. (Authenticated)
    """
    posts = db.query(Post).filter(Post.author_id == current_user.id).offset(skip).limit(limit).all()
    
    for post in posts:
        post.likes_count = db.query(Like).filter(Like.post_id == post.id).count()
        
    return posts

@router.get("/{slug}", response_model=PostSchema)
def read_post_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Retrieve a single post by slug. Only published posts are publicly accessible.
    """
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status != PostStatus.PUBLISHED:
        # If not published, only author or admin can view (this logic could be expanded)
        raise HTTPException(status_code=403, detail="Post not published")
        
    post.likes_count = db.query(Like).filter(Like.post_id == post.id).count()
    return post

@router.post("/", response_model=PostSchema)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_writer_user)
):
    """
    Create a new post. Requires WRITER or ADMIN role.
    New posts are set to PENDING status by default for moderation.
    """
    # Force status to PENDING if not specified or set to something else by non-admin
    status = PostStatus.PENDING
    if post_in.status == PostStatus.DRAFT:
        status = PostStatus.DRAFT
        
    db_post = Post(
        **post_in.model_dump(exclude={"status"}), 
        author_id=current_user.id,
        status=status,
        published=(status == PostStatus.PUBLISHED)
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

