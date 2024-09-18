import subprocess

def run_code(code: str, test_cases: list):
    results = []
    
    try:
        # Create a temporary Python file with the provided code
        with open("temp_code.py", "w") as f:
            f.write(code)
        
        # Check for syntax errors by compiling the code
        try:
            compile(code, 'temp_code.py', 'exec')
        except SyntaxError as e:
            return [{"error": f"SyntaxError: {e}"}]
        print("noerror")
        for test_case in test_cases:
            try:
                # Run the code with the test case input
                process = subprocess.run(
                    ["python", "temp_code.py"],
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
    
    return results