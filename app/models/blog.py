import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    WRITER = "writer"
    READER = "reader"

class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"

# Many-to-Many relationship for Bookmarks/Saved Posts
bookmarks = Table(
    "bookmarks",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    full_name = Column(String)
    avatar = Column(String, default="/avatars/default.jpg")
    google_id = Column(String, unique=True, nullable=True, index=True)  # Google OAuth ID
    role = Column(Enum(UserRole), default=UserRole.READER)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False) # Keeping for legacy, will transition to role
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    posts = relationship("Post", back_populates="author")
    bookmarked_posts = relationship("Post", secondary=bookmarks, back_populates="bookmarked_by")
    comments = relationship("Comment", back_populates="author")
    likes = relationship("Like", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    # Relationships
    posts = relationship("Post", back_populates="category")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    excerpt = Column(Text)
    content = Column(Text)
    image = Column(String)
    read_time = Column(String)
    featured = Column(Boolean, default=False)
    published = Column(Boolean, default=True) # Keeping for legacy, will transition to status
    status = Column(Enum(PostStatus), default=PostStatus.PUBLISHED) # Default to published for existing posts
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign Keys
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relationships
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    bookmarked_by = relationship("User", secondary=bookmarks, back_populates="bookmarked_posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    # Relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
