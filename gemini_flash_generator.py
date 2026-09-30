import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-flash-latest")


def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = (f"Give one concise, practical nutrition or recovery tip (2-3 sentences, "
              f"plain text) for someone whose fitness goal is: {goal}.")
    try:
        return genai.GenerativeModel(FLASH_MODEL).generate_content(prompt).text.strip()
    except Exception as e:
        return f"Could not fetch a tip right now ({e})."