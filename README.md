# 🚀 AI Lead Qualification API

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Status](https://img.shields.io/badge/Status-Live-success)
![Deployment](https://img.shields.io/badge/Deployed%20on-Render-black)

> Intelligent lead parsing and scoring system with built-in resilience  
> Designed for real-world sales pipelines and production deployment

---

## 🌐 Live Demo

🔗 **Live API:**  
https://lead-qualifier-api-1x4j.onrender.com  

📄 **Swagger Docs:**  
https://lead-qualifier-api-1x4j.onrender.com/docs  

👉 Test endpoint: `POST /qualify`

---

## 🧠 Overview

This project simulates a real-world **AI-powered lead qualification system**.

It processes raw user input and returns:
- Structured lead data  
- Lead quality score (0–100)  
- Category classification (Hot / Warm / Cold)  
- Reasoning behind the evaluation  

Built with **resilience in mind**, the system continues to function even when external AI services are unavailable.

---

## ⚙️ Features

- 🔄 Dual Processing Mode (OpenAI + Fallback)  
- 🛡️ 100% uptime using rule-based fallback logic  
- 🧠 Intelligent lead scoring & categorization  
- ⚡ FastAPI backend with interactive Swagger UI  
- 🌍 Public deployment on Render  

---

## 🧪 Example Usage

### Request

```json
{
  "message": "Looking for a 3BHK in Gurgaon, budget 1 crore, within 2 months"
}
```
##📦 Example Response
```json
{
  "result": {
    "source": "fallback",
    "data": {
      "lead_data": {
        "name": null,
        "requirement": "Property purchase",
        "budget": "Detected from input",
        "timeline": "Detected from input",
        "location": "Detected from input"
      },
      "evaluation": {
        "score": 70,
        "category": "Warm",
        "reasoning": "Rule-based evaluation using keywords"
      }
    }
  }
}
```

---

##🛠️ Tech Stack
-Backend: FastAPI
-Language: Python
-AI Integration: OpenAI (toggle-based)
-Deployment: Render
-API Testing: Swagger UI

---

##🚀 Run Locally
```
git clone https://github.com/bhavyach05/Lead-Qualifier.git
cd Lead-Qualifier

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

python -m uvicorn main:app --reload
```

---

##🔐 Environment Variables (Optional)

To enable AI mode:
```
OPENAI_API_KEY=your_api_key_here
```
Then in code:
```PYTHON
USE_OPENAI = True
```

---

##🌍 Deployment

Deployed on Render with public access.
Free tier note:

-Service may sleep after inactivity
-First request can take ~30–50 seconds

---

##🎯 Why this project stands out

-Not just an API → a resilient system design
-Works with or without external AI
-Structured output suitable for real-world pipelines
-Built with deployment and failure scenarios in mind

---

##📌 Future Improvements

-Advanced NLP parsing (names, exact budgets, locations)
-Database integration for lead storage
-Frontend dashboard for visualization
-Real-time CRM integration

---

##👨‍💻 Author

Bhavya Chaudhry
