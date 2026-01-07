import requests
import os

RAPIDAPI_KEY = "e276ce68a1msh48e499dbbd8c433p1e4c42jsn8f041d8d37c3"
RAPIDAPI_HOST = "chat-gpt26.p.rapidapi.com"
RAPIDAPI_URL = "https://chat-gpt26.p.rapidapi.com/"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
    "Content-Type": "application/json",
}


def call_llm(prompt: str):
    payload = {
        "model": "GPT-5-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        RAPIDAPI_URL,
        json=payload,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # chat-gpt26 returns text in choices[0].message.content
    return data["choices"][0]["message"]["content"]


def parse_resume(resume_text: str):
    prompt = f"""
You are an AI career advisor and recruiter assistant.

Analyze the resume below and return ONLY valid JSON in the following format:

{{
  "skills": ["skill1", "skill2", "..."],
  "total_experience_years": number,
  "professional_summary": "short summary",

  "recommended_roles": [
    {{
      "role": "Job title",
      "reason": "Why this role fits the candidate"
    }}
  ],

  "recommended_companies": [
    {{
      "company": "Company name",
      "industry": "Industry",
      "why": "Why the candidate is suitable"
    }}
  ],

  "career_roadmap": [
    {{
      "stage": "Short Term (0–6 months)",
      "focus": ["skills to improve"],
      "actions": ["specific actions"]
    }},
    {{
      "stage": "Mid Term (6–18 months)",
      "focus": ["skills to improve"],
      "actions": ["specific actions"]
    }},
    {{
      "stage": "Long Term (18+ months)",
      "focus": ["skills to master"],
      "actions": ["specific actions"]
    }}
  ]
}}

Resume:
{resume_text}

Rules:
- Do NOT add explanations outside JSON
- Skills must be inferred from resume
- Companies should be realistic and relevant
- Roadmap must be actionable
"""

    return call_llm(prompt)



def match_candidate_job(candidate, job):
    prompt = f"""
    Candidate Skills:
    {candidate.skills}

    Candidate Experience:
    {candidate.experience} years

    Job Required Skills:
    {job.skills_required}

    Respond ONLY in JSON:
    {{
      "match_score": 0-100,
      "reason": "short explanation"
    }}
    """
    return call_llm(prompt)
