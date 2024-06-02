import subprocess
import uuid
import os

def execute_python_program(code: str):
    # Create a file for the input code
    # Save code to a temporary file
    code_filename = f"/tmp/{uuid.uuid4()}.py"
    with open(code_filename, 'w') as f:
        f.write(code)

    # Create a Docker command to run the code
    docker_command = [
        'docker', 'run', '--rm',
        '-v', f'{code_filename}:/app/code.py',
        'python:3.11-slim',
        'python', '/app/code.py'
    ]

    try:
        result = subprocess.run(docker_command, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = e.stderr

    os.remove(code_filename)
    # print(output)
    return {'output': output}


import docker
import uuid
import os
import tempfile

def execute_python_program_with_docker_sdk(code: str) -> str:
    """
    Executes a Python program inside a Docker container and returns the output.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: The output of the executed Python code.
    """
    # Create a temporary file for the input code
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_code_file:
        temp_code_file.write(code.encode('utf-8'))
        code_filename = temp_code_file.name
    
    try:
        # Initialize the Docker client
        client = docker.from_env()
        
        # Run the container
        result = client.containers.run(
            "python:3.11-slim",
            f"python /app/{os.path.basename(code_filename)}",
            volumes={code_filename: {'bind': f'/app/{os.path.basename(code_filename)}', 'mode': 'ro'}},
            remove=True
        )
        
        return result.decode("utf-8")
    except docker.errors.ContainerError as e:
        return f"ContainerError: {e.stderr.decode('utf-8')}"
    except docker.errors.ImageNotFound as e:
        return f"ImageNotFound: {str(e)}"
    except docker.errors.APIError as e:
        return f"APIError: {str(e)}"
    finally:
        # Clean up the temporary file
        os.remove(code_filename)
