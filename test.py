import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro-latest")
response = model.generate_content("Hello, how does machine learning work?")
print(response.text)
