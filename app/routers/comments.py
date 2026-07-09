from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)

@router.post(
    "/blogs/{blog_id}",
    response_model=schemas.CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    blog_id: int,
    comment: schemas.CommentCreate,
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

    new_comment = models.Comment(
        content=comment.content,
        user_id=current_user.id,
        blog_id=blog_id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get(
    "/blogs/{blog_id}",
    response_model=list[schemas.CommentResponse],
)
def get_comments(
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

    comments = (
        db.query(models.Comment)
        .filter(models.Comment.blog_id == blog_id)
        .all()
    )

    return comments

@router.put(
    "/{comment_id}",
    response_model=schemas.CommentResponse,
)
def update_comment(
    comment_id: int,
    comment_update: schemas.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this comment",
        )

    comment.content = comment_update.content

    db.commit()
    db.refresh(comment)

    return comment

@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this comment",
        )

    db.delete(comment)
    db.commit()