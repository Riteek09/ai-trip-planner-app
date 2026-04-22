
# AI Trip Planner using Google Gemini API

An AI-powered trip planner built with Django. Users can register, log in, generate day-wise itineraries with Gemini, see live weather, estimate budgets, save trip history, and download trip plans as PDFs.

## Features
- User authentication (register/login/logout)
- AI-generated itinerary using Gemini API
- Weather summary using OpenWeather API
- Budget estimation
- Trip history dashboard
- PDF download for each trip
- Responsive Bootstrap UI

## Tech Stack
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Backend: Python, Django
- Database: SQLite
- AI API: Gemini API
- Weather API: OpenWeather API

## 1. Create virtual environment
```bash
python -m venv venv
```

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

## 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 3. Setup environment variables
Copy `.env.example` to `.env` and fill your keys.

### Windows PowerShell
```powershell
copy .env.example .env
```

### Mac/Linux
```bash
cp .env.example .env
```

## 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

## 6. Run the project
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Project Structure
```text
ai_trip_planner/
├── ai_trip_planner/
├── planner/
├── static/
├── templates/
├── .env.example
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Current API note
This project uses the newer `google-genai` Python SDK and a stable Gemini model string (`gemini-2.5-flash`). Google’s quickstart shows the GenAI SDK installation, and the model docs recommend stable model names such as `gemini-2.5-flash` for production-style use. citeturn805494view0turn569073view2
