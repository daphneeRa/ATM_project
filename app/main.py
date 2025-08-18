from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ATM FastAPI project is running 🚀"}
