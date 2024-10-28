import logging
import re
from typing import Optional
from datetime import datetime
from fastapi.responses import JSONResponse

from schemas.authentication import get_token_payload
from .connection import get_db
from models.users import Session
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session as DBSession
from starlette.middleware.base import BaseHTTPMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to get the token from the request
def get_token_from_request(request: Request) -> Optional[str]:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return None
    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    return token


# Function to check if the session has expired
async def is_session_expired(token: str, db: DBSession) -> bool:
    session = db.query(Session).filter(Session.session_token == token, Session.session_status == 1, Session.deleted_at.is_(None)).first()
    if session:
        if session.session_expiry < datetime.utcnow():
            session.session_status = False
            session.deleted_at = datetime.utcnow()
            session.updated_at = datetime.utcnow()
            db.commit()
            return True  # Session has expired
    else:
        session = db.query(Session).filter(Session.session_token == token).first()
        if session and session.session_expiry < datetime.utcnow():
            session.session_status = False
            session.deleted_at = datetime.utcnow()
            session.updated_at = datetime.utcnow()
            db.commit()
            return True
        return True # Session has expired
    return False  # Session is still active


# this for check token and verify token in this
async def auth_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response

    skip_paths = ["/", "/docs", "/redoc", "/openapi.json", "/favicon.ico"]

    if request.url.pathrequest.url.path in skip_paths or any(request.url.path.startswith(f"{path}/") for path in skip_paths):
        response = await call_next(request)
        return response

    token = get_token_from_request(request) 
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    payload = get_token_payload(token)
    request.state.user = payload


    db: DBSession = next(get_db())
    session_expired = await is_session_expired(token, db)
    if session_expired:
        return JSONResponse(content={"success": 2, "message": "Session expired! Please log in."}, status_code=200)
    response = await call_next(request)
    return response


# Exception Handling Middleware
class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"success": 2, "message": exc.detail},
            )
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": f"An unexpected error occurred. {exc}"},
            )
