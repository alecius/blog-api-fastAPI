from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"],
)

@router.post(
    "/",
    response_model=schemas.BlogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_blog(
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        owner_id=current_user.id,
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog