import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")


def ask_pro(prompt: str) -> str:
    try:
        return genai.GenerativeModel(PRO_MODEL).generate_content(prompt).text.strip()
    except Exception as e:  # missing key, quota, network...
        return f"Could not reach Gemini ({e}). Check GOOGLE_API_KEY and try again."


def generate_workout_gemini(age: int, weight: float, goal: str, intensity: str) -> str:
    prompt = f"""Create a personalized 7-day workout plan.
User: age {age}, weight {weight} kg, goal: {goal}, preferred intensity: {intensity}.

Format each day as plain text:
Day N - Focus
  Warm-up (5-10 mins): ...
  Main workout: exercise - sets x reps (or duration) - rest
  Cooldown/Recovery: ...
Include at least one rest or active-recovery day. Keep it safe, beginner-friendly
where intensity is low, and end with a one-line reminder to consult a doctor
before starting. No markdown symbols like ** or #."""
    return ask_pro(prompt)