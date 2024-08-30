import subprocess
import os

def run_code(code: str, test_cases: list):
    results = []
    try:
        # Create a temporary Java file with the provided code
        with open("TempCode.java", "w") as f:
            f.write(code)
        
        # Compile the Java code
        compile_process = subprocess.run(["javac", "TempCode.java"], capture_output=True)
        if compile_process.returncode != 0:
            raise Exception(compile_process.stderr.decode())
        
        for test_case in test_cases:
            try:
                # Run the compiled Java code with the test case input
                process = subprocess.run(
                    ["java", "TempCode"],
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
    except Exception as e:
        results.append({"error": str(e)})
    finally:
        # Clean up the temporary files
        if os.path.exists("TempCode.java"):
            os.remove("TempCode.java")
        if os.path.exists("TempCode.class"):
            os.remove("TempCode.class")
    
    return results