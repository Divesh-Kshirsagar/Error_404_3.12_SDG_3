# SmartQ - Telemedicine Queue Optimizer

An AI-powered telemedicine queue management system that uses voice input and Grok API for intelligent patient triage and prioritization.

## 🚀 Features

- **Voice Symptom Input**: Patients can describe symptoms using Web Speech API
- **AI-Powered Triage**: Grok API analyzes symptoms and assigns risk scores
- **Smart Queue Prioritization**: Cases split between Junior (≤0.7) and Senior (>0.7) doctors
- **Real-time Dashboard**: HTMX polling for live queue updates
- **Modern UI**: TailwindCSS with glassmorphism and smooth animations

## 📋 Tech Stack

- **Backend**: Django 5.x
- **Database**: SQLite
- **Frontend**: TailwindCSS, HTMX
- **Voice Input**: Web Speech API
- **AI**: Grok API (xAI)

## 🗺️ Sitemap

| Route | Description |
|-------|-------------|
| `/` | Patient Intake - Voice/text symptom submission |
| `/dashboard/` | Doctor Dashboard - Split queue view |
| `/api/queue-update/` | HTMX endpoint for queue polling |
| `/admin/` | Django Admin |

## 🏗️ Project Structure

```
smartq/
├── manage.py
├── requirements.txt
├── config/                 # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── clinic/                 # Main application
    ├── models.py           # Patient, Case models
    ├── views.py            # IntakeView, DashboardView
    ├── services.py         # Grok API integration
    ├── urls.py             # App routing
    └── templates/
        ├── base.html
        └── clinic/
            ├── intake.html
            ├── dashboard.html
            └── partials/
                └── queue_tables.html
```

## ⚙️ Setup

1. **Create and activate virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional, for Grok API):
   ```bash
   echo "GROK_API_KEY=your_api_key_here" > .env
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**:
   ```bash
   python manage.py runserver
   ```

7. **Visit**: http://127.0.0.1:8000

## 🎨 Design

### Flow Diagram

```
Patient → Voice Input (Web Speech API)
       ↓
  Text Transcript
       ↓
  HTMX POST → Django View
       ↓
  Grok API Analysis → {symptoms, risk_score}
       ↓
  Save to SQLite
       ↓
  Dashboard Queue (HTMX Polling)
       ↓
  Junior Queue (≤0.7) | Senior Queue (>0.7)
```

### Risk Score Guidelines

| Score | Level | Examples |
|-------|-------|----------|
| 0.0-0.3 | Low | Cold, mild headache |
| 0.4-0.6 | Medium | Fever, persistent cough |
| 0.7-0.8 | High | Severe pain, breathing difficulty |
| 0.9-1.0 | Critical | Chest pain, stroke symptoms |

## 📝 Development Notes

- Without a Grok API key, the system uses mock analysis based on keyword matching
- HTMX polling interval is set to 5 seconds for real-time updates
- Voice input requires HTTPS or localhost in most browsers

## 📄 License

MIT License
