import os
import google.generativeai as genai

# Get the API key from environment variable
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found in environment variables")

genai.configure(api_key=api_key)

def generate_content(prompt: str) -> str:
    try:
        # Create the model configuration
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
            "max_output_tokens": 6000,
            "response_mime_type": "text/plain",
        }

        # Use the Gemini API to generate content
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="Provide short, guiding questions and responses to help the student understand and resolve their issue with sorting algorithms.",
        )

        chat_session = model.start_chat(
            history=[
            ]
        )

        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Error generating content"