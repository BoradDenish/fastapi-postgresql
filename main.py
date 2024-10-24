from fastapi import FastAPI

from routers import authentication

app = FastAPI(debug=False)


@app.get("/")
def hello_world():
    return "Hello, world!"

# Include routers
app.include_router(authentication.router, prefix="")

