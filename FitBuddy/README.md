# FitBuddy - AI Fitness Plan Generator

AI-powered personalised fitness planning web application built with FastAPI and Google Gemini.

## Features

- Generate a customised 7-day workout plan using Google Gemini AI
- Nutrition and recovery tips tailored to your fitness goal
- Feedback-based plan refinement (updates the plan, preserving the original)
- Secure admin dashboard with cookie-based session authentication
- Premium dark navy and lime green UI design

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy 2.0, SQLite
- **AI**: Google Gemini API (gemini-3.8-flash)
- **Frontend**: Jinja2 templates, custom CSS
- **Auth**: itsdangerous session tokens (httponly cookies)
- **Tests**: pytest + httpx TestClient

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd FitBuddy
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
# Windows
venv\Scriptsctivate
# Linux/macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```
GOOGLE_API_KEY=your_actual_gemini_api_key
SECRET_KEY=a_random_string_at_least_32_characters
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
```

### 5. Run the application

```bash
python run.py
```

Open http://localhost:8000 in your browser.

## Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
FitBuddy/
app/
  __init__.py
  config.py          # Settings from environment variables
  models.py          # SQLAlchemy ORM models
  database.py        # DB session and CRUD helpers
  schemas.py         # Pydantic request validators
  auth.py            # Admin auth and session tokens
  gemini_generator.py        # Workout plan generation
  gemini_flash_generator.py  # Nutrition tip generation
  updated_plan.py            # Feedback-based plan update
  routes.py          # All FastAPI route handlers
  main.py            # FastAPI app entry point
templates/           # Jinja2 HTML templates
static/
  css/style.css
  js/script.js
tests/               # pytest test suite
run.py               # Uvicorn server launcher
requirements.txt
.env.example
README.md
```

## Security Notes

- API keys are stored in `.env` (never committed to git)
- Admin session uses httponly cookies with itsdangerous signing
- All user inputs are validated server-side
- AI-generated content is rendered as plain text (no raw HTML injection)

## Academic Project

Built for Tamil Nadu Skills - AI-ML and Generative AI track.
