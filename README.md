# FitBuddy – AI Fitness Plan Generator (FastAPI + Gemini)

## Setup
    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env            # then add your GOOGLE_API_KEY
    uvicorn main:app --reload

Open http://127.0.0.1:8000 (API docs at /docs, admin at /view-all-users).

Optional: drop a gym photo at static/images/gym.jpg for the background.
Model names are set in .env (GEMINI_PRO_MODEL / GEMINI_FLASH_MODEL).
