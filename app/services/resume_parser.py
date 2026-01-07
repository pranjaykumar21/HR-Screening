import os
import json
import http.client
import PyPDF2
import docx
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Text Extraction
# -------------------------------
def extract_text_from_pdf(path: str) -> str:
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    return " ".join(p.text for p in doc.paragraphs)

# -------------------------------
# GPT-4o via RapidAPI
# -------------------------------
def parse_resume(file_path: str):
    if file_path.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    else:
        resume_text = extract_text_from_docx(file_path)

    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        raise RuntimeError("RAPIDAPI_KEY missing")

    conn = http.client.HTTPSConnection("gpt-4o.p.rapidapi.com")

    prompt = f"""
Extract resume information and return STRICT JSON only.

JSON FORMAT:
{{
  "skills": [],
  "education": [],
  "experience": [],
  "projects": []
}}

Resume Text:
\"\"\"
{resume_text[:12000]}
\"\"\"
"""

    payload = json.dumps({
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "gpt-4o.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    conn.request("POST", "/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    conn.close()

    response_json = json.loads(data)

    content = response_json["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("LLM response not valid JSON")
