import os

import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "You are a professional career coach who writes cover letters.\n\n"
    "Rules you must follow without exception:\n"
    "- Output only the cover letter text. No commentary, no explanations.\n"
    "- Start directly with the salutation or a header — never with 'Here is' or similar.\n"
    "- Write in clean, formal business English using proper paragraphs.\n"
    "- Do not mention AI, ATS systems, or that this was generated.\n"
    "- Match the tone and seniority level implied by the CV and job description.\n"
)


def generate_cover_letter(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return "⚠ OPENROUTER_API_KEY is not set. Please check your .env file."

    model = os.getenv("OPENROUTER_MODEL", "minimax/minimax-m2.5")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "temperature": 0.4,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        return "⚠ The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"⚠ Network error: {e}"

    if "choices" not in data:
        error_msg = data.get("error", {}).get("message", "Unknown error")
        return f"⚠ API error: {error_msg}"

    return data["choices"][0]["message"]["content"].strip()