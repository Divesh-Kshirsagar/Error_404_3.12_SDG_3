# AarogyaQueue 🏥

A smart Telemedicine Queue Optimizer MVP that streamlines patient triage and doctor assignment using AI-powered symptom analysis.

## 🚀 Features

- **Smart Triage**: AI-powered symptom analysis (using Groq LLM) to determine severity.
- **Auto-Queueing**: Patients automatically assigned to JUNIOR or SENIOR doctors based on risk.
- **Voice-First Interface**: Patients can report symptoms via voice (using Groq Whisper).
- **ATM-Style UI**: Simplified, high-contrast, large-button interface for easy accessibility.
- **Role-Based Portals**:
  - **Patient Portal**: Register, login, report symptoms, view wait time.
  - **Doctor Portal**: View prioritized queue, patient details, prescribe medication.
  - **Admin Portal**: Dashboard analytics, manage doctors.

## 🛠️ Tech Stack

- **Frontend**: React (Vite), Tailwind CSS v4, TanStack Query
- **Backend**: FastAPI, SQLModel (SQLite)
- **AI/ML**: 
  - **Groq API**: Whisper (STT) + Llama 3 (LLM) for symptom extraction
  - **scikit-learn**: Fallback risk prediction model
- **Database**: SQLite (Zero config)

## 📋 Prerequisites

- Node.js v20+ (Required for Vite v7)
- Python 3.9+
- Groq API Key (Get one at [console.groq.com](https://console.groq.com))

## ⚡ Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
# Note: Use uv if available for faster install: uv pip install -r requirements.txt
pip install -r requirements.txt

# Run the server (auto-creates database on first run)
uvicorn main:app --reload
```
Backend will run at: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure API Keys
cp .env.local.example .env.local
# Edit .env.local and add your VITE_GROQ_API_KEY
```

**Create `.env.local`:**
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=AarogyaQueue
VITE_GROQ_API_KEY=your_groq_api_key_here
```

**Run Development Server:**
```bash
npm run dev
```
Frontend will run at: `http://localhost:5173`

## 📂 Project Structure

```
AarogyaQueue/
├── backend/                # FastAPI Application
│   ├── api/                # API Endpoints (auth, patients, doctors)
│   ├── ml/                 # Machine Learning Models
│   ├── services/           # Business Logic (Risk, Queue)
│   ├── utils/              # Constants & Helpers
│   ├── database.py         # DB Configuration
│   ├── main.py             # App Entry Point
│   └── models.py           # SQLModel Database Schemas
│
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # React Components (auth, patient, doctor, admin)
│   │   ├── services/       # API Clients & AI Logic
│   │   └── App.jsx         # Routing
│   └── index.css           # Tailwind v4 Styles
│
└── README.md
```

## 🧪 Testing

### Default Credentials (from Seed Data)

**Doctors:**
- **Senior**: ID `1` (PIN: `1234`)
- **Junior**: ID `3` (PIN: `1234`)

**Admin:**
- Dashboard accessible at `/admin` (No auth for MVP demo)

**Patient:**
- Register via the portal or use Seed Patient (Phone: `9876543210`, PIN: `1111`)

## 🛡️ License

MIT
