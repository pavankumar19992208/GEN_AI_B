from fastapi import FastAPI, APIRouter, HTTPException, Request
from GEN_AI.content_generator import generate_content

assist_router = APIRouter()

@assist_router.post("/assist")
async def assist(request: Request):
    try:
        # Get the data from the request
        data = await request.json()
        code = data.get("code")
        problem_statement = data.get("problemStatement")
        error = data.get("results")  # Assuming 'results' contains error information
        user_input = data.get("userInput", "")  # Get userInput if it exists, otherwise use an empty string
        conversation_history = data.get("conversationHistory", "")  # Get conversation history if it exists
        print("codee--", code)

        # Prepare the prompt for the Gemini API
        prompt = f"""
        ## Student Code:
        ```python
        {code}
        ```
        Use code with caution.
        Error Message:
        {error}
        Previous Conversation:
        {conversation_history}
        Analyze the code and error message. Consider the previous conversation.
        Generate a focused question to help the student understand the cause of the error.
        Keep the question concise and relevant.
        Question:
        [Gemini's potential next question based on the student's answer from previous conversation or code change and previous question asked to student. (if applicable)]
        Feedback:
        [Gemini's feedback on the last student response (mandatory)]
        """

        if user_input:
            prompt += f"User Input: {user_input}\n"
            prompt += "Provide feedback on the correctness of the student's answer (user input) or code change from previous code in 4-5 words and generate the next question.\n"

        # Add guiding questions to the prompt
        prompt += "\nPlease prioritize syntax errors and ask guiding questions to help the student understand and resolve the issue with sorting algorithms."

        # Use the Gemini API to generate content
        response_text = generate_content(prompt)
        # Extract feedback and question from the response
        feedback = ""
        question = response_text

        # Assuming the response contains feedback and question separated by a delimiter
        if "Feedback:" in response_text and "Question:" in response_text:
            parts = response_text.split("Question:")
            feedback = parts[0].replace("Feedback:", "").strip()
            question = parts[1].strip()

        # Combine feedback and question
        combined_response = f"{feedback}\n{question}"
        print(combined_response)
        # Return the combined response from the Gemini API to the frontend
        return {"response": combined_response}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")