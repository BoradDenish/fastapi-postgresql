import logging
from fastapi import FastAPI

from config.middleware import ExceptionHandlingMiddleware, auth_middleware
from routers import authentication
from config.logging_config import setup_logging
from starlette.middleware.base import BaseHTTPMiddleware


setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(debug=False)


app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware) 
app.add_middleware(ExceptionHandlingMiddleware)

# app.mount("/uploads", StaticFiles(directory="uploads", html=True), name="uploads")

@app.get("/")
def hello_world():
    return "Hello, world!"

# Include routers
app.include_router(authentication.router, prefix="")

