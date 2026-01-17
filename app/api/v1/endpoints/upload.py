from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List, Optional
from app.api import deps
from app.models.blog import User
from app.schemas.upload import FileUploadResponse, FileDeleteResponse
from app.services import imagekit_service

router = APIRouter()

@router.post("/image", response_model=FileUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = Form("images"),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Upload an image to ImageKit.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        content = await file.read()
        result = imagekit_service.upload_file(
            file=content,
            file_name=file.filename,
            folder=f"atlania/{folder}",
            tags=["image", f"user_{current_user.id}"]
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/video", response_model=FileUploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    folder: str = Form("videos"),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Upload a video to ImageKit.
    """
    if not file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a video"
        )
    
    try:
        content = await file.read()
        result = imagekit_service.upload_file(
            file=content,
            file_name=file.filename,
            folder=f"atlania/{folder}",
            tags=["video", f"user_{current_user.id}"]
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/file", response_model=FileUploadResponse)
async def upload_general_file(
    file: UploadFile = File(...),
    folder: str = Form("files"),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Upload any file to ImageKit.
    """
    try:
        content = await file.read()
        result = imagekit_service.upload_file(
            file=content,
            file_name=file.filename,
            folder=f"atlania/{folder}",
            tags=["file", f"user_{current_user.id}"]
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{file_id}", response_model=FileDeleteResponse)
async def delete_file(
    file_id: str,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Delete a file from ImageKit.
    """
    # Note: In a real app, you might want to verify that the user owns this file
    # by checking a database record of uploads.
    try:
        imagekit_service.delete_file(file_id)
        return {"success": True, "message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
