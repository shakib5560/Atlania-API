from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.blog import User, UserRole
from app.schemas.blog import UserCreate
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email address.
    
    Args:
        db: Database session
        email: User's email address
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID.
    
    Args:
        db: Database session
        user_id: User's ID
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_google_id(db: Session, google_id: str) -> Optional[User]:
    """
    Get a user by Google ID.
    
    Args:
        db: Database session
        google_id: Google OAuth ID
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.google_id == google_id).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user with hashed password.
    
    Args:
        db: Database session
        user_in: User creation schema with plain password
    
    Returns:
        Created user object
    """
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        avatar=user_in.avatar,
        is_active=user_in.is_active,
        role=user_in.role or UserRole.READER,
        is_admin=(user_in.role == UserRole.ADMIN)  # Keeping for legacy
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_oauth_user(
    db: Session,
    email: str,
    full_name: str,
    avatar: str = None,
    google_id: str = None
) -> User:
    """
    Create a new user from OAuth (without password).
    
    Args:
        db: Database session
        email: User's email
        full_name: User's full name
        avatar: User's avatar URL
        google_id: Google OAuth ID
    
    Returns:
        Created user object
    """
    db_user = User(
        email=email,
        full_name=full_name,
        avatar=avatar or "/avatars/default.jpg",
        google_id=google_id,
        is_active=True,
        role=UserRole.READER,  # Default to READER for OAuth
        is_admin=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_or_create_oauth_user(
    db: Session,
    email: str,
    full_name: str,
    avatar: str = None,
    google_id: str = None
) -> User:
    """
    Get existing user or create new one from OAuth data.
    First checks by google_id, then by email.
    
    Args:
        db: Database session
        email: User's email
        full_name: User's full name
        avatar: User's avatar URL
        google_id: Google OAuth ID
    
    Returns:
        User object (existing or newly created)
    """
    # First try to find by google_id
    if google_id:
        user = get_user_by_google_id(db, google_id)
        if user:
            return user
    
    # Then try to find by email
    user = get_user_by_email(db, email)
    if user:
        # Link Google ID if not already linked
        if google_id and not user.google_id:
            user.google_id = google_id
            db.commit()
            db.refresh(user)
        return user
    
    # Create new user
    return create_oauth_user(db, email, full_name, avatar, google_id)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    
    Args:
        db: Database session
        email: User's email
        password: Plain text password
    
    Returns:
        User object if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.hashed_password:  # OAuth-only user
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user_role(db: Session, user_id: int, role: UserRole) -> Optional[User]:
    """
    Update a user's role.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    user.role = role
    user.is_admin = (role == UserRole.ADMIN)  # Update legacy field
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session) -> List[User]:
    """
    Get all users (for admin management).
    """
    return db.query(User).all()
