# api/routes/auth.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, verify_password, create_access_token
from models.user import User
from schemas.user import UserCreate, UserLogin, Token, UserResponse
from api.dependencies import get_current_user, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and save to DB
    print(f"Normalizing password: {user.password}")
    hashed_pwd = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate Token
    access_token = create_access_token(data={"sub": new_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)) -> Token:
    # Fetch user from DB
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # Validate user and password
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    # Generate Token
    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

@router.post("/refresh", response_model=Token, dependencies=[Depends(oauth2_scheme)])
def refresh_token(current_user: User = Depends(get_current_user)):
    access_token = create_access_token(data={"sub": current_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

@router.post("/logout", dependencies=[Depends(oauth2_scheme)])
def logout(current_user: User = Depends(get_current_user)):
    """
    Because JWTs are stateless, the server does not store active sessions. 
    True 'logout' happens on the frontend by deleting the token from LocalStorage.
    This endpoint serves as an optional confirmation and validation that the token was valid.
    """
    return {"message": f"User {current_user.email} successfully logged out. Please remove the token on the client side."}

@router.get("/me", response_model=UserResponse, dependencies=[Depends(oauth2_scheme)])
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get the current logged-in user's information.
    """
    return current_user