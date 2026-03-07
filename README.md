# 🎯 TalentScout — AI Hiring Assistant

An intelligent chatbot that screens tech candidates by collecting profile info and generating tailored technical questions using **Groq's LLaMA-3** model, built with **Streamlit**.

---

## 📁 Folder Structure

```
talentscout/
├── app.py                  # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── chat_engine.py      # LLM logic, prompt engineering, stage management
│   └── data_handler.py     # Candidate data saving (anonymised)
├── data/                   # Auto-created; stores session JSON files
├── .env                    # Your API key goes here (never commit this)
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone / unzip the project

```bash
cd talentscout
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Open `.env` and replace the placeholder:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at https://console.groq.com

### 5. Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🤖 How It Works

The chatbot flows through 5 stages:

| Stage | What happens |
|---|---|
| **Greeting** | Alex introduces himself and starts the screening |
| **Profile** | Collects name, email, phone, experience, desired role, location |
| **Tech Stack** | Candidate lists their technologies |
| **Assessment** | 3–5 LLM-generated technical questions, tailored to their stack |
| **Complete** | Farewell message + session saved to `data/` |

Type **exit**, **quit**, or **bye** at any point to end gracefully.

---

## 🔐 Data Privacy

- Email and phone are **SHA-256 hashed** before saving.
- Sessions are stored as local JSON in the `data/` folder.
- No data is sent to any third party beyond the Groq API for LLM inference.

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Streamlit** — UI
- **Groq SDK** — LLaMA-3 70B inference
- **python-dotenv** — environment variable management

---

## 💡 Prompt Design

- A structured `SYSTEM_BASE` prompt keeps the assistant on-topic at all times.
- Stage-specific prompts guide information gathering one field at a time.
- Tech questions are generated with a JSON-output prompt that specifies difficulty tiers (basic → advanced) and parses the response safely.
- Fallback questions are provided if JSON parsing fails.
