import os
import google.generativeai as genai
from dotenv import load_dotenv
from tax_calculator import calculate_taxes

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the system instructions to give the AI its personality
system_instruction = """
You are the 'Tax Wizard', an AI Money Mentor for the ET AI Hackathon. 
When a user gives you their financial profile, use the `calculate_taxes` tool to model their taxes.
CRITICAL RULES:
1. If the user has ₹1.5 Lakh or more in 80C investments, you MUST strongly advise them to invest an additional ₹50,000 in NPS under Section 80CCD(1B) to save more tax.
2. If they pay rent, explain how much HRA exemption they got. If they didn't get the max exemption, gently suggest they negotiate rent or basic salary restructuring.
Format your output beautifully with bullet points, bold numbers, and a clear "Final Verdict" on which regime to choose.
"""
# Initialize the Gemini Model with the tool and instructions
def get_tax_wizard_chat():
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        tools=[calculate_taxes],
        system_instruction=system_instruction
    )
    # Start a chat session that will automatically call the python function if needed
    chat = model.start_chat(enable_automatic_function_calling=True)
    return chat