from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.blog import Category
from app.schemas.blog import Category as CategorySchema

router = APIRouter()

@router.get("/", response_model=List[CategorySchema])
def read_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories
