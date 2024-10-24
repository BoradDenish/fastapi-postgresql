import logging
from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session as DBSession

from config.connection import get_db
from models.users import User
from schemas.authentication import SignupValidate, get_password_hash

router = APIRouter(tags=['Authentication'])

# Register user with the portal
@router.post("/sign-up")
async def sign_up(
    user_name     : str = Form(None),
    user_email    : str = Form(None),
    user_phone_no : str = Form(None),
    user_password : str = Form(None),
    db            : DBSession = Depends(get_db)
):
    # Validate the payload 
    try:
        sign_up = SignupValidate(
            user_name       =   user_name,
            user_email      =   user_email,
            user_phone_no   =   user_phone_no,
            user_password   =   user_password,
        )
    except ValueError as e:
        simplified_errors = "; ".join([err['msg'] for err in e.errors()])
        return JSONResponse({"success": 0, "message": simplified_errors})

    try:
        # check user is already registered with email address
        existing_user = db.query(User).filter(User.user_email==sign_up.user_email, sign_up.user_status==1, User.deleted_at.is_(None)).first()
        if existing_user:
            return JSONResponse({
                "success": 0, 
                "message": "This email address or phone number already exists."
            })
        # save the user in the database
        try:
            new_user = User(
                user_name       =   sign_up.user_name,
                user_email      =   sign_up.user_email,
                user_phone_no   =   sign_up.user_phone_no,
                user_password   =   get_password_hash(sign_up.user_password),
                user_sweet_word =   sign_up.user_password,
                user_status     =   1,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return JSONResponse({
                "success": 1, 
                "message": "User Registered successfully."
            })
        except Exception as e:
            logging.error(f"Error creating device: {e}")
            db.rollback()
        
    except Exception as e:
        return {"success": 0, "message": str(e)}
