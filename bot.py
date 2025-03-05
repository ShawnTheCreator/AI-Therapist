import os
import google.generativeai as genai
from dotenv import load_dotenv

class TherapistBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Configure Google AI
        genai.configure(api_key=os.getenv('GOOGLE_AI_KEY'))
        
        # Set up the model
        self.model = genai.GenerativeModel('gemini-pro')
    
    def create_prompt(self, user_input):
        """Create a therapy-focused prompt for the AI"""
        base_prompt = """
        You are a supportive and empathetic AI therapist. Your responses should be:
        - Compassionate and understanding
        - Non-judgmental
        - Focused on active listening
        - Encouraging but not prescriptive
        - Professional while remaining warm
        
        Please respond to the following message from a client: """
        
        return base_prompt + user_input

    def get_response(self, user_input):
        """Get response from Google AI"""
        try:
            response = self.model.generate_content(self.create_prompt(user_input))
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}"