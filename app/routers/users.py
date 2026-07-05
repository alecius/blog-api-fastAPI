from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import hash_password
from app.dependencies import get_db
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

#CREATE USER
@router.post(
    "/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#FETCH LIST OF USER
@router.get(
    "/",
    response_model=list[schemas.UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    users = db.query(models.User).all()

    return users

#fetch current user by JWT Token
@router.get(
    "/me",
    response_model=schemas.UserResponse,
)
def get_me(
    current_user: models.User = Depends(get_current_user),
):
    return current_user


#FETCH USER BY ID
@router.get("/{user_id}",
            response_model=schemas.UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

#UPDATE USER
@router.put(
    "/{user_id}",
    response_model=schemas.UserResponse,
)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.username = user_update.username
    user.email = user_update.email

    db.commit()
    db.refresh(user)

    return user

#DELETE USER
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()

