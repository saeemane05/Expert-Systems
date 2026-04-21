"""
UI Rendering Module
- HTML generation
- Styling
- Page templates
"""

from logic import KEY_SYMPTOMS, get_symptom_options


def render_question(question, index, answers):
    """
    Render the symptom question page
    
    Args:
        question: Current symptom name
        index: Current question index
        answers: List of previous answers
    
    Returns:
        HTML string
    """
    options = get_symptom_options(question)
    options_html = "".join(
        [f'<option value="{opt}">{opt}</option>' for opt in options.keys()]
    )

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
            <div class="progress">Question {index + 1} of {len(KEY_SYMPTOMS)}</div>
            <form method="post">
                <label for="severity">How severe is your {question.replace('_', ' ')}?</label>
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
