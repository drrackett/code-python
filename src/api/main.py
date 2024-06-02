# from fastapi import FastAPI

# from pydantic import BaseModel

# from src.libs.utils import execute_python_program, execute_python_program_with_docker_sdk

# app = FastAPI()

# class Code(BaseModel):
#     content: str

# @app.get("/api/python")
# def hello_world():
#     return {"message": "Hello World"}


# @app.post("/api/test", status_code = 200)
# async def test_code(code: Code):
#     output = execute_python_program_with_docker_sdk(code.content)
#     return {"output": output}


# @app.post("/api/submit")
# async def submit_code():
#     return {"message": "Hello World"}


from fastapi import FastAPI
from src.api.routers import router

app = FastAPI()

# Include the API router
app.include_router(router)

# Example root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to CodePython!"}