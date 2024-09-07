import google.generativeai as genai

genai.configure(api_key="AIzaSyCWdRGOjQ6W7fPIN2ooevW16_acWTvcgEQ")

def generate_content(prompt: str) -> str:
    try:
        # Use the Gemini API to generate content
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Error generating content"