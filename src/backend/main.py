from fastapi import FastAPI
from src.backend.api.v1.endpoints import run_code, submit_code

app = FastAPI()

# Include the API router
app.include_router(run_code.router, prefix="/api", tags=["run_code"])
app.include_router(submit_code.router, prefix="/api", tags=["submit_code"])

# Example root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to CodePython!"}