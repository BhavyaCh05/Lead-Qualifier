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
import re

def fallback_function(message: str):
    msg = message.lower()

    # -----------------------------
    # 🧠 Extract Budget
    # -----------------------------
    budget = None
    budget_match = re.search(r'(\d+(\.\d+)?\s*(lakh|lakhs|crore|cr))', msg)

    if budget_match:
        budget = budget_match.group(0)

    # -----------------------------
    # 📍 Extract Location
    # -----------------------------
    cities = ["gurgaon", "delhi", "mumbai", "bangalore", "pune", "noida", "hyderabad"]
    location = next((city for city in cities if city in msg), None)

    # -----------------------------
    # ⏳ Extract Timeline
    # -----------------------------
    timeline = None

    if "immediate" in msg or "asap" in msg:
        timeline = "immediate"
    else:
        timeline_match = re.search(r'(\d+\s*(day|days|week|weeks|month|months))', msg)
        if timeline_match:
            timeline = timeline_match.group(0)

    # -----------------------------
    # 🏠 Extract Requirement
    # -----------------------------
    requirement = None
    req_match = re.search(r'(\d+\s*(bhk))', msg)

    if req_match:
        requirement = req_match.group(0)

    # -----------------------------
    # 🎯 Scoring Logic
    # -----------------------------
    score = 40

    if budget:
        score += 20
    if timeline:
        if "immediate" in timeline:
            score += 30
        else:
            score += 20
    if location:
        score += 10
    if requirement:
        score += 10

    # Cap score
    score = min(score, 100)

    # -----------------------------
    # 🔥 Categorization
    # -----------------------------
    if score >= 80:
        category = "Hot"
    elif score >= 60:
        category = "Warm"
    else:
        category = "Cold"

    # -----------------------------
    # 🧠 Reasoning Generator
    # -----------------------------
    reasoning_parts = []

    if budget:
        reasoning_parts.append("Budget specified")
    if timeline:
        reasoning_parts.append("Clear timeline")
    if location:
        reasoning_parts.append("Location identified")
    if requirement:
        reasoning_parts.append("Requirement defined")

    reasoning = ", ".join(reasoning_parts) if reasoning_parts else "Limited information provided"

    return {
        "source": "fallback",
        "data": {
            "lead_data": {
                "name": None,
                "requirement": requirement or "Not specified",
                "budget": budget or "Not specified",
                "timeline": timeline or "Not specified",
                "location": location or "Not specified"
            },
            "evaluation": {
                "score": score,
                "category": category,
                "reasoning": reasoning
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