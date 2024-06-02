from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.libs.utils import execute_python_program_with_docker_sdk, run_container

router = APIRouter()

class Code(BaseModel):
    content: str

@router.post("/api/test", status_code=200)
def test_code(code: Code):
    """
    Endpoint to execute Python code inside a Docker container.

    Args:
        code (Code): The Python code to execute.

    Returns:
        dict: The output of the executed code.
    """
    try:
        # output = execute_python_program_with_docker_sdk(code.content)
        output = run_container(code.content)
        return {"output": output["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
