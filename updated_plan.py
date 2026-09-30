from gemini_generator import ask_pro


def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""Here is a user's current 7-day workout plan:

{original_plan}

The user's feedback: "{feedback}"

Revise the plan to reflect the feedback. Keep the same plain-text day-by-day
format (warm-up, main workout with sets/reps, cooldown) and keep it safe.
Return only the full updated plan."""
    return ask_pro(prompt)
