import subprocess
import tempfile
import os

def run_cpp_code(code: str, test_input: str) -> dict:
    """
    Writes the C++ code to a temporary file, mounts it to a Docker container,
    compiles it, and runs it against the provided input.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        code_path = os.path.join(temp_dir, "solution.cpp")
        with open(code_path, "w") as f:
            f.write(code)

        # 1. Compile inside Docker
        compile_cmd = [
            "docker", "run", "--rm", 
            "-v", f"{temp_dir}:/usr/src/app", 
            "-w", "/usr/src/app", 
            "gcc:latest", 
            "g++", "-O3", "-std=c++17", "solution.cpp", "-o", "solution"
        ]
        
        compile_process = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_process.returncode != 0:
            return {"status": "compilation_error", "logs": compile_process.stderr}

        # 2. Execute inside Docker with strict limits
        run_cmd = [
            "docker", "run", "--rm", 
            "-i",             # Keep STDIN open
            "--memory=256m",  # Limit memory to catch bounds/leaks
            "-v", f"{temp_dir}:/usr/src/app", 
            "-w", "/usr/src/app", 
            "gcc:latest", 
            "./solution"
        ]
        
        try:
            run_process = subprocess.run(
                run_cmd, input=test_input, capture_output=True, text=True, timeout=5
            )
            if run_process.returncode != 0:
                return {"status": "execution_error", "logs": run_process.stderr or "Non-zero exit code (e.g. Segfault)"}
            
            return {"status": "success", "logs": run_process.stdout}
            
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "logs": "Execution timed out. Possible infinite loop."}