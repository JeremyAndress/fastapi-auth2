from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from db.session import get_db
from schemas.user import UserCreate, UserList, UserListPag, Login
from schemas.response import Response_SM
from schemas.token import TokenUser
from core.security import create_access_token
from api.deps import get_admin_user
from .controller import (
    create_user, authenticate, get_user_cn,
    get_all_user_cn, delete_user_cn, update_user_cn
)
router = APIRouter()

#Controller

@router.post("/login/", response_model=TokenUser, tags=["auth"])
def login(user: Login, db: Session = Depends(get_db)):
    user = authenticate(db, user.username, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": create_access_token(user.username),
        "token_type": "bearer",
        "rol_id": user.rol.id if user.rol else None,
        "rol_name": user.rol.name if user.rol else None
    }

#Document

@router.get("/user/{id}", response_model=UserList, tags=["user"])
def user_get(
    id: int, 
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    user = get_user_cn(db, id)
    return user

@router.post("/user", response_model=Response_SM, tags=["user"])
def user_create(user: UserCreate, db: Session = Depends(get_db)):
    response = create_user(db, user)
    if not response.status:
        raise HTTPException(status_code=400, detail=response.result)
    return response


@router.delete("/user/{id}", response_model=Response_SM, tags=["user"])
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = delete_user_cn(id, db)
    if not response.status:
        raise HTTPException(status_code=400, detail=response.result)
    return response


@router.put("/user", response_model=Response_SM, tags=["user"])
def update_user(
    upd_user: UserList,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = update_user_cn(upd_user, db)
    if not response.status:
        raise HTTPException(status_code=400, detail=response.result)
    return response

#Collection

@router.get("/users", response_model=UserListPag, tags=["user"])
def get_all_user(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    user = get_all_user_cn(page, db)
    return user

