"""
Expert Medical Diagnosis System
Main application routes and setup
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from logic import get_next_question, get_symptom_options, diagnose, KEY_SYMPTOMS
from ui import render_question, render_result

app = FastAPI()


@app.get("/")
def start():
    """Start the diagnosis questionnaire"""
    return HTMLResponse(render_question(KEY_SYMPTOMS[0], 0, []))


@app.post("/")
async def process(
    request: Request,
    severity: str = Form(...),
    index: int = Form(...),
    answers: str = Form("")
):
    """
    Process the submitted answer and move to next question or show result
    
    Args:
        severity: Current severity selection
        index: Current question index
        answers: Comma-separated list of previous answers
    
    Returns:
        HTML response with next question or diagnosis result
    """
    # Get current symptom and its options
    current_symptom = KEY_SYMPTOMS[index]
    options = get_symptom_options(current_symptom)
    score = options.get(severity, 0)

    # Parse previous answers
    answers_list = [int(a) for a in answers.split(',')] if answers else []
    answers_list.append(score)
    
    # Move to next question
    index += 1

    # If all questions answered, show diagnosis
    if index >= len(KEY_SYMPTOMS):
        diagnosis = diagnose(answers_list)
        return HTMLResponse(render_result(diagnosis))

    # Otherwise, show next question
    next_question = get_next_question(index)
    return HTMLResponse(render_question(next_question, index, answers_list))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)