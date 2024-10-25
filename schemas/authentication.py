import os
import re
from typing import Optional
from pydantic import BaseModel, validator, root_validator
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM  = "HS256"
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


# Function to validate email format
def email_validation(user_email: str) -> Optional[str]:
    cus_email_lower = user_email.lower()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, cus_email_lower):
        return None
    return user_email


# Password hashing and verification functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Varify Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



class SignupValidate(BaseModel):
    user_name       : Optional[str]
    user_email      : Optional[str]
    user_password   : Optional[str]

    @validator('user_email', pre=True, always=True)
    def check_user_email(cls, v):
        if v and not email_validation(v):
            raise ValueError('Please provide a proper email.')
        return v

    @root_validator(pre=True)
    def check_required_fields(cls, values):
        if not values.get('user_name'):
            raise ValueError("Please provide a user name.")
        if not values.get('user_password'):
            raise ValueError("Please provide a user password.")
        if not values.get('user_email'):
            raise ValueError("Please provide a user email.")
        return values



class SigninValidation(BaseModel):
    user_email      : Optional[str]
    user_password   : Optional[str]

    @root_validator(pre=True)
    def check_required_fields(cls, values):
        if not values.get('user_email'):
            raise ValueError("Please provide a user email.")

        if not values.get('user_password'):
            raise ValueError("Please provide a user password.")
        return values
