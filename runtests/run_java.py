import subprocess
import os
import re

def run_code(code: str, test_cases: list):
    results = []
    try:
        # Extract the class name from the provided Java code
        class_name_match = re.search(r'public\s+class\s+(\w+)', code)
        if not class_name_match:
            raise Exception("No public class found in the provided code.")
        
        class_name = class_name_match.group(1)
        java_file_name = f"{class_name}.java"
        
        # Create a temporary Java file with the provided code
        with open(java_file_name, "w") as f:
            f.write(code)
        
        # Compile the Java code
        compile_process = subprocess.run(["javac", java_file_name], capture_output=True)
        if compile_process.returncode != 0:
            raise Exception(compile_process.stderr.decode())
        
        for test_case in test_cases:
            try:
                # Run the compiled Java code with the test case input
                process = subprocess.run(
                    ["java", class_name],
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
        if os.path.exists(java_file_name):
            os.remove(java_file_name)
        if os.path.exists(f"{class_name}.class"):
            os.remove(f"{class_name}.class")
    
    return results