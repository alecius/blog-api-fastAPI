from fastapi import FastAPI
from app.routers import users,auth

app = FastAPI(
    title="Blog API",
    description="Production-ready Blog API using FastAPI",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Blog API",
        "status": "Running Successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }