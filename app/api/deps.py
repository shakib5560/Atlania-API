from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.settings import settings
from app.core.security import verify_password
from app.models.blog import User, UserRole
from app.schemas.blog import TokenPayload
from app.services.user_service import get_user_by_id

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        db: Database session
        token: JWT token from Authorization header
    
    Returns:
        Current user object
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=int(user_id))
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_id(db, user_id=token_data.sub)
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current user from get_current_user dependency
    
    Returns:
        Current active user
    
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get the current admin user.
    
    Args:
        current_user: Current active user from get_current_active_user dependency
    
    Returns:
        Current admin user
    
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_writer_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get the current writer user.
    
    Args:
        current_user: Current active user from get_current_active_user dependency
    
    Returns:
        Current writer user
    
    Raises:
        HTTPException: If user is not a writer or admin
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.WRITER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
