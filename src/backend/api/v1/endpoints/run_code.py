from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.libs.utils import run_container

router = APIRouter()

class Code(BaseModel):
    content: str

@router.post("/test", status_code=200)
def test_code(code: Code):
    """
    Endpoint to execute Python code inside a Docker container.

    Args:
        code (Code): The Python code to execute.

    Returns:
        dict: The output of the executed code.
    """
    try:
        # Execute the code inside the Docker container
        output = run_container(code.content)
        
        # Check if the output is None
        if output["output"] is None:
            return {"output": output["error"]}
        
        return {"output": output["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))