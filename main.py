from fastapi import FastAPI

app = FastAPI(debug=False)


@app.get("/")
def hello_world():
    return "Hello, world!"


