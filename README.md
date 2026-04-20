# Hospital Expert System

A web-based expert system for medical diagnosis using symptom-based questioning.

## Features

- Interactive symptom assessment with severity levels (Not at all, Mild, Moderate, Severe)
- Diagnosis based on 99 diseases and 166 unique symptoms
- Confidence scoring and explanations
- Advice, recommended doctor, and urgency level for each diagnosis
- Beautiful UI with gradient backgrounds and responsive design

## Installation

1. Install Python dependencies:
   ```
   pip install fastapi uvicorn pandas
   ```

2. Run the application:
   ```
   uvicorn app:app --reload
   ```

3. Open http://127.0.0.1:8000 in your browser

## Files

- `app.py`: Main FastAPI application
- `symptoms_disease.csv`: Knowledge base of diseases and their symptoms
- `disease_advice.csv`: Advice, doctor, and urgency for each disease
- `templates/index.html`: HTML template (inline in app.py)

## How it works

1. The system asks about 166 symptoms one by one
2. User selects severity level for each symptom
3. System calculates disease scores based on average symptom severity
4. Returns the top matching disease with confidence, advice, and recommendations

## Testing

The system has been tested with automated scripts and manual interaction. It successfully diagnoses based on symptom patterns.