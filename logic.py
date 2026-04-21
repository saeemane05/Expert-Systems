"""
Business Logic Module
- Data loading
- Diagnosis algorithm
- Symptom scoring
"""

import pandas as pd

# Load data from CSVs
symptoms_df = pd.read_csv('symptoms_disease.csv')
advice_df = pd.read_csv('disease_advice.csv')

# Select key symptoms for efficient diagnosis
KEY_SYMPTOMS = [
    'fever', 'cough', 'headache', 'nausea', 'fatigue', 'chest_pain', 
    'shortness_of_breath', 'abdominal_pain', 'diarrhea', 'vomiting', 
    'rash', 'dizziness', 'joint_pain', 'sore_throat', 'loss_of_appetite'
]

# Custom options for different symptoms
SYMPTOM_OPTIONS = {
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
SEVERITY_OPTIONS = {
    "Not at all": 0,
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3
}


def get_next_question(index):
    """Get the next symptom question by index"""
    if index < len(KEY_SYMPTOMS):
        return KEY_SYMPTOMS[index]
    return None


def get_symptom_options(symptom):
    """Get options for a specific symptom"""
    return SYMPTOM_OPTIONS.get(symptom, SEVERITY_OPTIONS)


def diagnose(answers):
    """
    Core diagnosis algorithm
    Analyzes symptom scores and returns diagnosis with confidence
    
    Args:
        answers: List of severity scores for each symptom
    
    Returns:
        dict with disease info, confidence, advice, etc.
    """
    # Map symptoms to their scores
    symptom_scores = {KEY_SYMPTOMS[i]: answers[i] for i in range(len(answers))}

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
            disease_scores[disease] = score / count

    # Find best match
    if disease_scores:
        best_disease = max(disease_scores, key=disease_scores.get)
        confidence = (disease_scores[best_disease] / 3) * 100
    else:
        best_disease = "Unknown"
        confidence = 0

    # Get advice from database
    advice_row = advice_df[advice_df['disease'] == best_disease]
    if not advice_row.empty:
        advice = advice_row.iloc[0]['advice']
        doctor = advice_row.iloc[0]['doctor']
        urgency = advice_row.iloc[0]['urgency']
        severity = symptoms_df[symptoms_df['disease'] == best_disease]['severity'].iloc[0] \
            if not symptoms_df[symptoms_df['disease'] == best_disease].empty else 'unknown'
    else:
        advice = "Consult a doctor."
        doctor = "General Physician"
        urgency = "routine"
        severity = "unknown"

    # Generate explanation
    matched_symptoms = [sym for sym, score in symptom_scores.items() if score > 0]
    high_symptoms = [sym for sym, score in symptom_scores.items() if score >= 2]
    explanation = f"Based on your reported symptoms: {', '.join(matched_symptoms)}. "
    if high_symptoms:
        explanation += f"Particularly severe symptoms include: {', '.join(high_symptoms)}. "
    explanation += f"The system analyzed symptom patterns and matched this profile to {best_disease.replace('_', ' ').title()}, which commonly presents with these symptoms. This diagnosis is based on the average severity of matching symptoms across our knowledge base of {len(symptoms_df)} diseases."

    return {
        'disease': best_disease,
        'confidence': round(confidence, 1),
        'advice': advice,
        'doctor': doctor,
        'urgency': urgency,
        'severity': severity,
        'explanation': explanation,
        'matched_symptoms': matched_symptoms,
        'high_symptoms': high_symptoms
    }
