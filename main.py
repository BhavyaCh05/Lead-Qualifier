from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Optional OpenAI import
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

# Load env variables
load_dotenv()

app = FastAPI()

# Toggle (you can switch this anytime)
USE_OPENAI = False

# Initialize OpenAI client if available
client = None

if USE_OPENAI and OPENAI_AVAILABLE:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Request model
class ChatRequest(BaseModel):
    message: str


# Fallback Logic
def fallback_function(message: str):
    message_lower = message.lower()

    score = 50
    category = "Cold"

    if "budget" in message_lower or "crore" in message_lower or "lakhs" in message_lower:
        score += 20

    if "month" in message_lower or "immediate" in message_lower:
        score += 20

    if score >= 80:
        category = "Hot"
    elif score >= 60:
        category = "Warm"

    return {
        "source": "fallback",
        "data": {
            "lead_data": {
                "name": None,
                "requirement": "Property purchase",
                "budget": "Detected from input",
                "timeline": "Detected from input",
                "location": "Detected from input"
            },
            "evaluation": {
                "score": score,
                "category": category,
                "reasoning": "Rule-based evaluation using keywords"
            }
        }
    }


# Main Processing Function
def process_lead(message: str):
    if USE_OPENAI and OPENAI_AVAILABLE:
        try:
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

            response = client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )

            return {
                "source": "openai",
                "data": response.output_text
            }

        except Exception as e:
            # fallback if API fails
            return fallback_function(message)

    else:
        return fallback_function(message)


# Routes
@app.get("/")
def home():
    return {"message": "AI Lead Qualification API is running 🚀"}


@app.post("/qualify")
def qualify_lead(req: ChatRequest):
    result = process_lead(req.message)
    return {"result": result}