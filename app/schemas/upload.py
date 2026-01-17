from pydantic import BaseModel
from typing import Optional, List

class FileUploadResponse(BaseModel):
    file_id: str
    name: str
    url: str
    thumbnail_url: Optional[str] = None
    file_type: str
    size: int
    width: Optional[int] = None
    height: Optional[int] = None

class FileDeleteResponse(BaseModel):
    success: bool
    message: str
