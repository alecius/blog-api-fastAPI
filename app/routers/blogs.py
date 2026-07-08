from fastapi import APIRouter, Depends, status, HTTPException
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

@router.get(
    "/",
    response_model=list[schemas.BlogResponse],
)
def get_blogs(
    skip: int = 0,
    limit: int = 10,
    search: str = "",
    db: Session = Depends(get_db),
):
    blogs = (
        db.query(models.Blog)
        .filter(models.Blog.title.ilike(f"%{search}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return blogs

@router.get(
    "/{blog_id}",
    response_model=schemas.BlogResponse,
)
def get_blog(
    blog_id: int,
    db: Session = Depends(get_db),
):
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == blog_id)
        .first()
    )

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    return blog

@router.put(
    "/{blog_id}",
    response_model=schemas.BlogResponse,
)
def update_blog(
    blog_id: int,
    blog_update: schemas.BlogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == blog_id)
        .first()
    )

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )
    
    if blog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this blog",
        )

    blog.title = blog_update.title
    blog.content = blog_update.content

    db.commit()
    db.refresh(blog)

    return blog

@router.delete(
    "/{blog_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == blog_id)
        .first()
    )

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    if blog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this blog",
        )

    db.delete(blog)
    db.commit()