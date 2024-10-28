from datetime import datetime, timedelta
import logging
from typing import Dict
from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session as DBSession
from jose import jwt
from config.connection import get_db
from models.users import Session, User
from schemas.authentication import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, SigninValidation, SignupValidate, get_password_hash, verify_password

router = APIRouter(tags=['Authentication'])

# Register user with the portal
@router.post("/sign-up")
async def sign_up(
    user_name     : str = Form(...),
    user_email    : str = Form(...),
    user_password : str = Form(...),
    db            : DBSession = Depends(get_db)
):
    # Validate the payload 
    try:
        sign_up = SignupValidate(
            user_name       =   user_name,
            user_email      =   user_email,
            user_password   =   user_password,
        )
    except ValueError as e:
        simplified_errors = "; ".join([err['msg'] for err in e.errors()])
        return JSONResponse({"success": 0, "message": simplified_errors})

    # check user is already registered with email address
    existing_user = db.query(User).filter(User.user_email==sign_up.user_email, User.user_status==True, User.deleted_at.is_(None)).first()
    if existing_user:
        return JSONResponse({
            "success": 0, 
            "message": "This email address already exists."
        })
    else:
        # save the user in the database
        new_user = User(
            user_name       =   sign_up.user_name,
            user_email      =   sign_up.user_email,
            user_password   =   get_password_hash(sign_up.user_password),
            simple_password =   sign_up.user_password,
            user_status     =   1,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse({
            "success": 1, 
            "message": "User Registered successfully."
        })
        # try:
        # except Exception as e:
        #     logging.error(f"Error creating device: {e}")
        #     db.rollback()
        
    # try:
    # except Exception as e:
    #     return {"success": 0, "message": str(e)}



# Login in to the portal
@router.post('/sign-in')
def sign_in(
    db           : DBSession = Depends(get_db), 
    user_email   : str = Form(...), 
    user_password: str = Form(...),
    ):
    # Validate the payload
    try:
        SigninValidation(
            user_email      =   user_email,
            user_password   =   user_password,
        )
    except ValueError as e:
        simplified_errors = "; ".join([err['msg'] for err in e.errors()])
        return JSONResponse({
            "success": 0, 
            "message": simplified_errors
        })

    user = db.query(User).filter(User.user_email==user_email, User.user_status==True, User.deleted_at.is_(None)).first()
    if not user:
        return JSONResponse({
            "success": 0,
            "message": "Please check email address."
        })
    # verify the password
    if not verify_password(user_password, user.user_password):
            return JSONResponse({
            "success": 0,
            "message": "Invalid password."
        })

    token        = create_access_token({"user_id": user.user_id, "user_email": user.user_email})
    user_session = create_user_session(db, user, token)

    return JSONResponse({
        "success"      : 1,
        "message"      : "Login Successful.",
        "session_token": token,
        "user_id"      : str(user.user_id),
    })

# Function to create a new access token
def create_access_token(data: Dict[str, str], expiry_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to create a new user session
def create_user_session(db: DBSession, user: User, token: str, expiry_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> DBSession:
    session_expiry = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    new_session = Session(
        session_email   = user.user_email,
        session_token   = token,
        session_user    = user.user_id,
        session_expiry  = session_expiry,
        session_status  = True,
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


