# app/main.py
from fastapi import FastAPI
from .routers import accounts

# Create a FastAPI app instance with a title and description
app = FastAPI(
    title="Financial Accounts API",
    description="A simple API to manage financial accounts."
)

# Include the accounts router
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])

@app.get("/")
def read_root():
    """A simple root endpoint."""
    return {"message": "Welcome to the Financial Accounts API. Check the /docs endpoint for details."}