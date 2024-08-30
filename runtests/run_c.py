import subprocess
import os

def run_code(code: str, test_cases: list):
    results = []
    try:
        # Create a temporary C file with the provided code
        with open("temp_code.c", "w") as f:
            f.write(code)
        
        # Compile the C code
        compile_process = subprocess.run(["gcc", "temp_code.c", "-o", "temp_code"], capture_output=True)
        if compile_process.returncode != 0:
            raise Exception(compile_process.stderr.decode())
        
        for test_case in test_cases:
            try:
                # Run the compiled C code with the test case input
                process = subprocess.run(
                    ["./temp_code"],
                    input=test_case.input,
                    text=True,
                    capture_output=True
                )
                
                # Check the output
                output = process.stdout.strip()
                if output == test_case.expectedOutput:
                    results.append({"input": test_case.input, "output": output, "result": "pass"})
                else:
                    results.append({"input": test_case.input, "output": output, "result": "fail", "expected": test_case.expectedOutput})
            except Exception as e:
                results.append({"input": test_case.input, "error": str(e)})
    finally:
        # Clean up the temporary files
        if os.path.exists("temp_code.c"):
            os.remove("temp_code.c")
        if os.path.exists("temp_code"):
            os.remove("temp_code")
    
    return results