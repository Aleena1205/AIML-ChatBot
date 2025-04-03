import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY is missing in .env file!")

# Configure Gemini API with the key
genai.configure(api_key=API_KEY)

def get_aiml_response(user_message):
    """
    Sends a user message to Gemini API and gets a response.
    Ensures only AIML (Artificial Intelligence & Machine Learning) related questions are answered.
    """
    aiml_filter_prompt = """
    You are an AI tutor specializing in AIML (Artificial Intelligence & Machine Learning).
    You must:
    1. Answer only AIML-related questions.
    2. If the question is NOT related to AIML, respond with:
       "I only assist with AIML topics. Please ask an AI or ML-related question."
    3. Provide structured, clear, and concise explanations.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  
        response = model.generate_content(aiml_filter_prompt + "\n\nUser: " + user_message)
        return response.text.strip()
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Test the API connection
if __name__ == "__main__":
    test_question = "What is a neural network?"
    print(f"👤 User: {test_question}")
    print(f"🤖 AI: {get_aiml_response(test_question)}")
