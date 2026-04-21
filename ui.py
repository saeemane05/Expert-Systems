"""
UI Rendering Module
- HTML generation
- Styling
- Page templates
"""

from logic import KEY_SYMPTOMS, get_symptom_options

QUESTIONS_PER_PAGE = 5  # Show 5 questions per page


def render_questions_batch(batch_num, answers):
    """
    Render multiple symptom questions on one page (batch view)
    
    Args:
        batch_num: Batch number (0 for first 5, 1 for next 5, etc.)
        answers: List of previous answers
    
    Returns:
        HTML string with multiple questions
    """
    start_idx = batch_num * QUESTIONS_PER_PAGE
    end_idx = min(start_idx + QUESTIONS_PER_PAGE, len(KEY_SYMPTOMS))
    
    # Build question fields HTML
    questions_html = ""
    for i in range(start_idx, end_idx):
        symptom = KEY_SYMPTOMS[i]
        options = get_symptom_options(symptom)
        options_html = "".join(
            [f'<option value="{opt}">{opt}</option>' for opt in options.keys()]
        )
        questions_html += f"""
        <div class="question-block">
            <label for="symptom_{i}">Q{i + 1}. How severe is your {symptom.replace('_', ' ')}?</label>
            <select name="symptom_{i}" id="symptom_{i}" class="symptom-select" required>
                <option value="">-- Select --</option>
                {options_html}
            </select>
        </div>
        """
    
    # Determine button text and condition
    is_last_batch = end_idx >= len(KEY_SYMPTOMS)
    button_text = "Get Diagnosis" if is_last_batch else "Next Questions"
    
    # Build hidden fields for previous answers
    hidden_fields = ""
    for i in range(len(answers)):
        hidden_fields += f'<input type="hidden" name="prev_answer_{i}" value="{answers[i]}">\n'
    
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
                max-width: 700px;
                margin: auto;
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h2 {{
                margin-bottom: 10px;
                font-size: 2em;
            }}
            .progress {{
                margin-bottom: 25px;
                font-size: 0.95em;
                color: #e8f0fe;
            }}
            .questions-group {{
                background: rgba(255, 255, 255, 0.05);
                padding: 25px;
                border-radius: 10px;
            }}
            .question-block {{
                margin-bottom: 25px;
                text-align: left;
            }}
            .question-block label {{
                display: block;
                margin-bottom: 8px;
                font-size: 1.05em;
                font-weight: 500;
            }}
            .question-block select {{
                width: 100%;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                background-color: white;
                color: #333;
                cursor: pointer;
                transition: box-shadow 0.3s;
            }}
            .question-block select:focus {{
                outline: none;
                box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            }}
            .button-group {{
                display: flex;
                gap: 15px;
                margin-top: 30px;
                justify-content: center;
            }}
            button {{
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                font-size: 1.05em;
                cursor: pointer;
                transition: all 0.3s;
                font-weight: 600;
            }}
            .btn-next {{
                background: #4CAF50;
                color: white;
            }}
            .btn-next:hover {{
                background: #45a049;
                transform: scale(1.05);
            }}
            .btn-back {{
                background: #2196F3;
                color: white;
            }}
            .btn-back:hover {{
                background: #0b7dda;
                transform: scale(1.05);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🩺 Expert Medical Diagnosis</h2>
            <div class="progress">Questions {start_idx + 1} - {end_idx} of {len(KEY_SYMPTOMS)}</div>
            
            <form method="post" class="questions-group">
                {questions_html}
                
                {hidden_fields}
                <input type="hidden" name="batch_num" value="{batch_num}">
                
                <div class="button-group">
                    {f'<button type="submit" name="action" value="back" class="btn-back">← Back</button>' if batch_num > 0 else ''}
                    <button type="submit" name="action" value="next" class="btn-next">{button_text} →</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """


def render_result(diagnosis):
    """
    Render the diagnosis result page
    
    Args:
        diagnosis: Dictionary with diagnosis results from logic.diagnose()
    
    Returns:
        HTML string
    """
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
                text-align: left;
                font-size: 0.9em;
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
                <h3>{diagnosis['disease'].replace('_', ' ').title()}</h3>
                <p class="confidence">Confidence: {diagnosis['confidence']}%</p>
                <p><b>Severity:</b> {diagnosis['severity'].title()}</p>
                <p><b>Advice:</b> {diagnosis['advice']}</p>
                <p><b>Recommended Doctor:</b> {diagnosis['doctor']}</p>
                <p><b>Urgency:</b> {diagnosis['urgency'].title()}</p>
                <div class="explanation">
                    <p><b>Explanation:</b> {diagnosis['explanation']}</p>
                </div>
            </div>
            <form action="/">
                <button type="submit">Start Over</button>
            </form>
        </div>
    </body>
    </html>
    """
