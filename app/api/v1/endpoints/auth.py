from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.settings import settings
from app.core.security import create_access_token
from app.schemas.blog import User, UserCreate, Token, UserLogin
from app.services.user_service import (
    create_user,
    authenticate_user,
    get_user_by_email,
    get_or_create_oauth_user
)
from app.services.google_oauth import oauth, get_google_user_info
from app.api.deps import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user.
    
    Args:
        user_in: User registration data
        db: Database session
    
    Returns:
        Created user object
    
    Raises:
        HTTPException: If email already registered
    """
    # Check if user already exists
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    Args:
        db: Database session
        form_data: OAuth2 form with username (email) and password
    
    Returns:
        Access token
    
    Raises:
        HTTPException: If credentials are invalid
    """
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=User)
def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current authenticated user.
    
    Args:
        current_user: Current active user from JWT token
    
    Returns:
        Current user object
    """
    return current_user


@router.post("/test-token", response_model=User)
def test_token(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Test access token validity.
    
    Args:
        current_user: Current active user from JWT token
    
    Returns:
        Current user object
    """
    return current_user


@router.get("/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth login flow.
    Redirects user to Google's consent screen.
    
    Args:
        request: FastAPI request object
    
    Returns:
        Redirect to Google OAuth
    """
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth is not configured"
        )
    
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    if not redirect_uri:
        redirect_uri = str(request.url_for('google_callback'))
    
    with open("oauth_debug.log", "a") as f:
        f.write(f"DEBUG: Redirecting to Google with redirect_uri: {redirect_uri}\n")
    
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle Google OAuth callback.
    Creates or retrieves user and returns JWT token.
    
    Args:
        request: FastAPI request object
        db: Database session
    
    Returns:
        Redirect with JWT token or error
    """
    try:
        # Exchange authorization code for access token
        print(f"DEBUG: Handling Google callback. Request URL: {request.url}")
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from token
        user_info = await get_google_user_info(token)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        # Extract user data
        email = user_info.get('email')
        full_name = user_info.get('name', '')
        avatar = user_info.get('picture', '/avatars/default.jpg')
        google_id = user_info.get('sub')  # Google's user ID
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
        # Get or create user
        user = get_or_create_oauth_user(
            db=db,
            email=email,
            full_name=full_name,
            avatar=avatar,
            google_id=google_id
        )
        
        # Generate JWT token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        frontend_url = settings.FRONTEND_URL or "http://localhost:3000"
        separator = "&" if "?" in frontend_url else "?"
        return RedirectResponse(
            url=f"{frontend_url}{separator}token={access_token}"
        )
        
    except Exception as e:
        # Redirect to frontend with error
        frontend_url = settings.FRONTEND_URL or "http://localhost:3000"
        separator = "&" if "?" in frontend_url else "?"
        return RedirectResponse(
            url=f"{frontend_url}{separator}error={str(e)}"
        )
