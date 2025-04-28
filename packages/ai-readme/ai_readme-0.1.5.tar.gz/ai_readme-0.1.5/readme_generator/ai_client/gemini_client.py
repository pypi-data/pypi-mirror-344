import os
import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')

    def chat(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text