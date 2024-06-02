import docker
import os
import tempfile

IMAGE_NAME = "python_execution_env:latest"

# Function to build the Docker image
def build_image():
    client = docker.from_env()
    try:
        # Check if the image already exists
        client.images.get(IMAGE_NAME)
        print("Image already exists.")
    except docker.errors.ImageNotFound:
        try:
            print("Starting to build Docker image...")
            image, build_logs = client.images.build(path="./src/libs/", tag=IMAGE_NAME)
            for log in build_logs:
                print(log.get('stream', ''), end='')
            print("Image built successfully.")
        except docker.errors.BuildError as e:
            print(f"Error building image: {e}")
            raise
        except docker.errors.APIError as e:
            print(f"API Error: {e}")
            raise
    except docker.errors.APIError as e:
        print(f"Error checking for image: {e}")
        raise


# Function to run a Docker container with a temporary file and return the output
def run_container(code):
    # Ensure the image is built
    # build_image()
    
    # Create a temporary file with the code
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    try:
        client = docker.from_env()
        container = client.containers.run(
            image=IMAGE_NAME,
            command=["python", os.path.basename(temp_file_path)],
            volumes={os.path.dirname(temp_file_path): {'bind': '/app', 'mode': 'ro'}},
            working_dir="/app",
            detach=True,
            stdout=True,
            stderr=True
        )
        
        # Wait for the container to finish execution
        container.wait()
        
        # Capture the logs
        logs = container.logs(stdout=True, stderr=True)
        output = logs.decode("utf-8")

        container.remove()

        return {"output": output, "error": None}
    except docker.errors.ContainerError as e:
        return {"output": None, "error": str(e)}
    except docker.errors.ImageNotFound as e:
        return {"output": None, "error": str(e)}
    except docker.errors.APIError as e:
        return {"output": None, "error": str(e)}
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

###################################################################################################


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
