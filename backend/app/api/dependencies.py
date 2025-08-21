from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import uuid
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import ValidationError

from app.users import models, schemas, crud
from app.security import TokenData # Re-using TokenData from security
from app.settings import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login" # The URL for the token endpoint
)

def get_db_from_request(request: Request) -> Session:
    """
    Dependency to retrieve the database session from the request state.
    The session is attached to the request by the RLS middleware.
    """
    return request.state.db

def get_current_user(
    db: Session = Depends(get_db_from_request), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Dependency to get the current user from a JWT token.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials: Invalid subject",
            )

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = crud.get_user(db, user_id=uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Dependency to get the current user, but only if they are a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
