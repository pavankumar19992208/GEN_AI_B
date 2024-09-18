import subprocess
import json

def run_code(code: str, test_cases: list):
    results = []
    
    try:
        # Create a temporary JavaScript file with the provided code
        with open("temp_code.js", "w") as f:
            f.write(code)
        
        # Check for syntax errors by running the code with a dummy input
        process = subprocess.run(
            ["node", "-c", "temp_code.js"],
            text=True,
            capture_output=True
        )
        
        if process.returncode != 0:
            # If there is a syntax error, return the error message
            return [{"error": process.stderr.strip()}]
        
        for test_case in test_cases:
            try:
                print("en-", test_case.input)
                # Run the code with the test case input
                process = subprocess.run(
                    ["node", "temp_code.js"],
                    input=test_case.input,
                    text=True,
                    capture_output=True
                )
                
                # Check the output
                output = process.stdout.strip()
                print("output:", output)
                print("expected output", test_case.expectedOutput)
                
                # Parse the output and expected output as JSON
                output_json = json.loads(output)
                expected_output_json = json.loads(test_case.expectedOutput)
                
                if output_json == expected_output_json:
                    results.append({"input": test_case.input, "output": output, "result": "pass"})
                else:
                    results.append({"input": test_case.input, "output": output, "result": "fail", "expected": test_case.expectedOutput})
            except Exception as e:
                results.append({"input": test_case.input, "error": str(e)})
    except Exception as e:
        results.append({"error": str(e)})
    
    return results