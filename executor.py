import subprocess
import tempfile
import os

def run_cpp_code(source_code: str, test_input: str = "") -> dict:
    """
    Writes C++ code to a temporary directory, mounts it to Docker, 
    compiles and executes it safely.
    """
    # Create a temporary directory that will automatically be cleaned up
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write the C++ source code
        cpp_file_path = os.path.join(temp_dir, "solution.cpp")
        with open(cpp_file_path, "w") as f:
            f.write(source_code)
            
        # Write the test input
        input_file_path = os.path.join(temp_dir, "input.txt")
        with open(input_file_path, "w") as f:
            f.write(test_input)
            
        # 1. Compilation Step (Inside Docker)
        compile_cmd = [
            "docker", "run", "--rm",
            "-v", f"{temp_dir}:/app", # Mount the temp dir to /app in container
            "agentic-cpp-sandbox",
            "g++", "-O2", "-std=c++17", "solution.cpp", "-o", "solution"
        ]
        
        try:
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=5)
            if compile_result.returncode != 0:
                return {"status": "compilation_error", "logs": compile_result.stderr}
        except subprocess.TimeoutExpired:
            return {"status": "compilation_error", "logs": "Compiler timed out."}

        # 2. Execution Step (Inside Docker with strict limits)
        run_cmd = [
            "docker", "run", "--rm",
            "-v", f"{temp_dir}:/app",
            "--memory=512m", "--cpus=1.0",
            "--network=none", # Security: Disconnect container from internet
            "agentic-cpp-sandbox",
            "sh", "-c", "./solution < input.txt"
        ]
        
        try:
            run_result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=3)
            if run_result.returncode != 0:
                return {"status": "runtime_error", "logs": run_result.stderr}
            return {"status": "success", "logs": run_result.stdout}
        except subprocess.TimeoutExpired:
            return {"status": "time_limit_exceeded", "logs": "Execution timed out (TLE)."}