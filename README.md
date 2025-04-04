# 🧠 Simulation App (LangChain + FastAPI + Pinecone)

A fully customizable simulation engine powered by OpenAI, LangChain, and Pinecone. The app guides users through step-by-step decision-making journeys in domains like career, relationships, travel, and more.

---

## ✅ Features

- 🔁 **Dynamic Simulations**: Admin can create reusable simulation templates (e.g. career, travel, etc.)
- 🧠 **AI-Powered Guidance**: Uses GPT-4/GPT-3.5 for contextual responses based on simulation steps
- 🧩 **UI-Aware Responses**: GPT adapts to active UI components like sliders, dropdowns, text inputs
- 🧠 **Long-Term Memory**: Pinecone stores user chat history for personalized and contextual simulations
- 📩 **Email Notifications**: AWS SES integration for onboarding, alerts, and progress updates
- 🆔 **Structured User Tracking**: Auto-generated user IDs like #WI0000001 for tracking simulation progress
- 🔐 **Security**: Token-based sessions, rate limiting, and data retention policies
- 📦 **FastAPI Backend**: REST API structure for front-end integration (React, Vue, etc.)
- 📁 **HTML or JSON Response Support**: GPT can return UI-ready HTML or structured JSON for frontend rendering

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI Engine**: LangChain + OpenAI (GPT-3.5 / GPT-4o)
- **Memory**: Pinecone Vector DB
- **Database**: MongoDB
- **Email**: Amazon SES
- **Frontend**: Any (React recommended)

---

## 🚀 Getting Started

### 1. Clone the Project
```bash
git clone https://github.com/your-repo/simulation-app
cd simulation-app
```

### 2. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file:
```ini
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=your_index_name
MONGO_URI=your_mongodb_uri
AWS_REGION=your_ses_region
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### 5. Run FastAPI Server
```bash
uvicorn main:app --reload
```

Server will be available at `http://127.0.0.1:8000`

---

## 📂 Project Structure
```
├── main.py                # FastAPI entrypoint
├── chains/
│   └── simulation_chain.py
├── utils/
│   └── memory.py
│   └── db.py
├── templates/             # Simulation templates
├── .env                   # Env variables
├── requirements.txt
└── README.md
```

---

## 🧪 Testing API
Use [Postman](https://www.postman.com/) or [Swagger UI](http://127.0.0.1:8000/docs) to test endpoints like:
- `/simulate/` – Run user simulation
- `/admin/template/create/` – Create new simulation template
- `/user/history/` – Fetch user chat history

---

