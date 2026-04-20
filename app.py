from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import pandas as pd
import csv

app = FastAPI()

# Load data from CSVs
symptoms_df = pd.read_csv('symptoms_disease.csv')
advice_df = pd.read_csv('disease_advice.csv')

# Select key symptoms for efficient diagnosis (10-15 common symptoms)
key_symptoms = [
    'fever', 'cough', 'headache', 'nausea', 'fatigue', 'chest_pain', 
    'shortness_of_breath', 'abdominal_pain', 'diarrhea', 'vomiting', 
    'rash', 'dizziness', 'joint_pain', 'sore_throat', 'loss_of_appetite'
]
all_symptoms = key_symptoms

# Custom options for different symptoms
symptom_options = {
    'fever': {"None": 0, "Low (100-101°F)": 1, "Moderate (102-103°F)": 2, "High (104°F+)": 3},
    'cough': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'headache': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'nausea': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'fatigue': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'chest_pain': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'shortness_of_breath': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'abdominal_pain': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'diarrhea': {"None": 0, "Occasional": 1, "Frequent": 2, "Severe": 3},
    'vomiting': {"None": 0, "Occasional": 1, "Frequent": 2, "Severe": 3},
    'rash': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'dizziness': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'joint_pain': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'sore_throat': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    'loss_of_appetite': {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
}

# Severity options
severity_options = {
    "Not at all": 0,
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3
}

# Function to get next question
def get_next_question(index):
    if index < len(all_symptoms):
        return all_symptoms[index]
    return None

# Render question page
def render_question(q, index, answers):
    options = symptom_options.get(q, severity_options)
    options_html = "".join([f'<option value="{opt}">{opt}</option>' for opt in options.keys()])
    return f"""
    <html>
    <head>
        <title>Expert Diagnosis System</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
                margin: 0;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h2 {{
                margin-bottom: 20px;
                font-size: 2em;
            }}
            label {{
                display: block;
                margin: 20px 0 10px;
                font-size: 1.2em;
            }}
            select {{
                width: 100%;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                margin-bottom: 20px;
            }}
            button {{
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
                font-size: 1.1em;
                cursor: pointer;
                transition: background 0.3s;
            }}
            button:hover {{
                background: #45a049;
            }}
            .progress {{
                margin-bottom: 20px;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🩺 Expert Medical Diagnosis</h2>
            <div class="progress">Question {index + 1} of {len(all_symptoms)}</div>
            <form method="post">
                <label for="severity">How severe is your {q.replace('_', ' ')}?</label>
                <select name="severity" id="severity">
                    {options_html}
                </select>
                <input type="hidden" name="index" value="{index}">
                <input type="hidden" name="answers" value="{','.join([str(a) for a in answers])}">
                <button type="submit">Next</button>
            </form>
        </div>
    </body>
    </html>
    """

# Render result
def render_result(answers):
    # answers is list of scores for each symptom
    symptom_scores = {all_symptoms[i]: answers[i] for i in range(len(answers))}

    # Calculate scores for each disease
    disease_scores = {}
    for _, row in symptoms_df.iterrows():
        disease = row['disease']
        score = 0
        count = 0
        for sym in ['symptom1', 'symptom2', 'symptom3']:
            if pd.notna(row[sym]):
                score += symptom_scores.get(row[sym], 0)
                count += 1
        if count > 0:
            disease_scores[disease] = score / count  # average severity

    # Find best match
    if disease_scores:
        best_disease = max(disease_scores, key=disease_scores.get)
        confidence = (disease_scores[best_disease] / 3) * 100  # max average is 3
    else:
        best_disease = "Unknown"
        confidence = 0

    # Get advice
    advice_row = advice_df[advice_df['disease'] == best_disease]
    if not advice_row.empty:
        advice = advice_row.iloc[0]['advice']
        doctor = advice_row.iloc[0]['doctor']
        urgency = advice_row.iloc[0]['urgency']
        severity = symptoms_df[symptoms_df['disease'] == best_disease]['severity'].iloc[0] if not symptoms_df[symptoms_df['disease'] == best_disease].empty else 'unknown'
    else:
        advice = "Consult a doctor."
        doctor = "General Physician"
        urgency = "routine"
        severity = "unknown"

    # Explanation
    matched_symptoms = [sym for sym, score in symptom_scores.items() if score > 0]
    high_symptoms = [sym for sym, score in symptom_scores.items() if score >= 2]
    explanation = f"Based on your reported symptoms: {', '.join(matched_symptoms)}. "
    if high_symptoms:
        explanation += f"Particularly severe symptoms include: {', '.join(high_symptoms)}. "
    explanation += f"The system analyzed symptom patterns and matched this profile to {best_disease.replace('_', ' ').title()}, which commonly presents with these symptoms. This diagnosis is based on the average severity of matching symptoms across our knowledge base of {len(symptoms_df)} diseases."

    return f"""
    <html>
    <head>
        <title>Diagnosis Result</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
                margin: 0;
            }}
            .container {{
                max-width: 700px;
                margin: auto;
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h2 {{
                margin-bottom: 20px;
                font-size: 2em;
            }}
            .result {{
                background: white;
                color: black;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .confidence {{
                font-size: 1.5em;
                color: #4CAF50;
                font-weight: bold;
            }}
            .advice {{
                margin-top: 20px;
                text-align: left;
            }}
            .explanation {{
                margin-top: 20px;
                font-style: italic;
            }}
            button {{
                background: #2196F3;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
                font-size: 1.1em;
                cursor: pointer;
                margin-top: 20px;
            }}
            button:hover {{
                background: #0b7dda;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Final Diagnosis</h2>
            <div class="result">
                <h3>{best_disease.replace('_', ' ').title()}</h3>
                <p class="confidence">Confidence: {round(confidence, 1)}%</p>
                <p><b>Severity:</b> {severity.title()}</p>
                <p><b>Advice:</b> {advice}</p>
                <p><b>Recommended Doctor:</b> {doctor}</p>
                <p><b>Urgency:</b> {urgency.title()}</p>
                <div class="explanation">
                    <p><b>Explanation:</b> {explanation}</p>
                </div>
            </div>
            <form action="/">
                <button type="submit">Start Over</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.get("/")
def start():
    return HTMLResponse(render_question(all_symptoms[0], 0, []))

@app.post("/")
async def process(request: Request, severity: str = Form(...), index: int = Form(...), answers: str = Form("")):
    current_symptom = all_symptoms[index]
    options = symptom_options.get(current_symptom, severity_options)
    score = options.get(severity, 0)
    answers_list = [int(a) for a in answers.split(',')] if answers else []
    answers_list.append(score)
    index += 1

    if index >= len(all_symptoms):
        return HTMLResponse(render_result(answers_list))

    next_q = get_next_question(index)
    return HTMLResponse(render_question(next_q, index, answers_list))