from authlib.integrations.starlette_client import OAuth
from app.core.settings import settings
from typing import Optional, Dict, Any

# Initialize OAuth
oauth = OAuth()

# Register Google OAuth client
if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


async def get_google_user_info(token: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Get user information from Google using the access token.
    
    Args:
        token: OAuth token dictionary containing access_token
    
    Returns:
        User information dictionary with email, name, picture, etc.
    """
    try:
        # The token already contains the user info in the 'userinfo' key
        # when using OpenID Connect
        if 'userinfo' in token:
            return token['userinfo']
        return None
    except Exception as e:
        print(f"Error getting Google user info: {e}")
        return None
