from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class ChatRequest(BaseModel):
    message: str


def process_lead(message: str):
    prompt = f"""
You are an AI system that extracts and evaluates sales leads.

Return STRICT JSON:

{{
  "lead_data": {{
    "name": null,
    "requirement": "",
    "budget": "",
    "timeline": "",
    "location": ""
  }},
  "evaluation": {{
    "score": 0,
    "category": "Hot/Warm/Cold",
    "reasoning": ""
  }}
}}

Message:
{message}
"""

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        return {
            "source": "openai",
            "data": response.output_text
        }

    except Exception as e:
        # Fallback logic (VERY IMPORTANT for demo reliability)
        return {
            "source": "fallback",
            "error": str(e),
            "data": {
                "lead_data": {
                    "name": None,
                    "requirement": "Property purchase",
                    "budget": "Approx detected",
                    "timeline": "Estimated",
                    "location": "Detected from input"
                },
                "evaluation": {
                    "score": 70,
                    "category": "Warm",
                    "reasoning": "Fallback used due to API limitation"
                }
            }
        }


@app.get("/")
def home():
    return {"message": "AI Lead Qualification API is running 🚀"}


@app.post("/qualify")
def qualify_lead(req: ChatRequest):
    result = process_lead(req.message)
    return {"result": result}