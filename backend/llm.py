# llm.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_cover_letter(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct"),
        "temperature": 0.4,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional human career coach.\n\n"
                    "Write a REAL cover letter exactly as a human would send it.\n\n"
                    "ABSOLUTE RULES (MUST FOLLOW):\n"
                    "- Do NOT write any introductory or explanatory sentences.\n"
                    "- Do NOT say 'Here is', 'Below is', 'ATS-friendly', or similar.\n"
                    "- Start DIRECTLY with a header or 'Dear Hiring Manager,'.\n"
                    "- Write in clean business English with proper paragraphs.\n"
                    "- Output ONLY the letter text.\n"
                    "- Do NOT mention AI, ATS, or generation.\n"
                )
            },
            {"role": "user", "content": prompt}
        ],
    }

    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    data = res.json()
    if "choices" not in data:
        return "⚠ Failed to generate cover letter. Please try again."

    return data["choices"][0]["message"]["content"].strip()
