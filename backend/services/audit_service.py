import json
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

AUDIT_PROMPT_TEMPLATE = """
You are an expert environmental auditor and ESG analyst.
Analyze the following text extracted from a corporate sustainability report:

---
{report_text}
---

Provide your analysis strictly in valid JSON format with the following keys:
{
  "transparency_score": <number between 0 and 100>,
  "summary": "<summary of findings>",
  "greenwashing_detected": <true or false>,
  "claims_analyzed": [
    {
      "claim": "<text of claim>",
      "verdict": "<verified | unverified | greenwashing>",
      "reasoning": "<explanation>"
    }
  ]
}
Return only the raw JSON object. Do not include markdown code fences or conversational text.
"""

class AuditService:
    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY in your .env file."
            )

        genai.configure(api_key=key)

        generation_config = {
            "temperature": 0.0,
            "top_p": 1.0,
        }

        self.model = genai.GenerativeModel(
            "gemini-3.6-flash",
            generation_config=generation_config
        )

    def analyze_report(self, text: str) -> dict:
        prompt = AUDIT_PROMPT_TEMPLATE.replace("{report_text}", text[:15000])
        response = self.model.generate_content(prompt)

        raw_output = response.text.strip()
        raw_output = re.sub(r"^```json\s*", "", raw_output, flags=re.MULTILINE)
        raw_output = re.sub(r"^```\s*", "", raw_output, flags=re.MULTILINE)
        raw_output = raw_output.strip()

        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {
                "transparency_score": 0,
                "summary": "Failed to parse model output into JSON.",
                "greenwashing_detected": False,
                "claims_analyzed": [],
                "raw_response": raw_output
            }