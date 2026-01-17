from imagekitio import ImageKit
from app.core.settings import settings
from typing import Optional, Dict, Any, List
import uuid

# Initialize ImageKit client
ik = ImageKit(
    public_key=settings.IMAGEKIT_PUBLIC_KEY,
    private_key=settings.IMAGEKIT_PRIVATE_KEY,
    url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
)

def upload_file(
    file: Any, 
    file_name: str, 
    folder: str = "general",
    tags: List[str] = None,
    is_private_file: bool = False
) -> Dict[str, Any]:
    """
    Upload a file to ImageKit.
    
    Args:
        file: The file content (bytes, file-like object, or base64 string)
        file_name: The name to give the file in ImageKit
        folder: The folder to store the file in
        tags: List of tags to associate with the file
        is_private_file: Whether the file should be private
        
    Returns:
        Dict containing upload results (url, fileId, name, etc.)
    """
    # Ensure unique filename
    unique_name = f"{uuid.uuid4()}-{file_name}"
    
    upload_options = {
        "file": file,
        "file_name": unique_name,
        "options": {
            "folder": folder,
            "tags": tags or [],
            "is_private_file": is_private_file,
            "use_unique_file_name": True
        }
    }
    
    result = ik.upload(**upload_options)
    
    if result.error:
        raise Exception(f"ImageKit upload error: {result.error.message}")
        
    return {
        "file_id": result.response.file_id,
        "name": result.response.name,
        "url": result.response.url,
        "thumbnail_url": result.response.thumbnail_url,
        "file_type": result.response.file_type,
        "size": result.response.size,
        "width": result.response.width,
        "height": result.response.height,
    }

def delete_file(file_id: str) -> bool:
    """
    Delete a file from ImageKit.
    
    Args:
        file_id: The ID of the file to delete
        
    Returns:
        True if successful
    """
    result = ik.delete_file(file_id)
    
    if result.error:
        raise Exception(f"ImageKit delete error: {result.error.message}")
        
    return True

def get_file_details(file_id: str) -> Dict[str, Any]:
    """
    Get details of a file from ImageKit.
    """
    result = ik.get_file_details(file_id)
    
    if result.error:
        raise Exception(f"ImageKit details error: {result.error.message}")
        
    return result.response.__dict__

def get_transformed_url(path: str, transformations: List[Dict[str, Any]]) -> str:
    """
    Generate a transformed URL for an image.
    
    Example transformations: [{"width": 100, "height": 100, "crop": "at_max"}]
    """
    options = {
        "path": path,
        "transformation": transformations
    }
    return ik.url(options)
