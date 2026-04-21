"""
Expert Medical Diagnosis System
Main application routes and setup
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from logic import diagnose, KEY_SYMPTOMS
from ui import render_questions_batch, render_result

app = FastAPI()


@app.get("/")
def start():
    """Start the diagnosis questionnaire with first batch of questions"""
    return HTMLResponse(render_questions_batch(0, []))


@app.post("/")
async def process(
    request: Request,
    batch_num: int = Form(...),
    action: str = Form(...)
):
    """
    Process submitted questions and move to next batch or show results
    
    Args:
        batch_num: Current batch number
        action: "next" to continue or "back" to go back
    """
    # Get form data
    form_data = await request.form()
    
    # Extract all previous answers
    all_answers = []
    prev_answer_idx = 0
    while f"prev_answer_{prev_answer_idx}" in form_data:
        all_answers.append(int(form_data[f"prev_answer_{prev_answer_idx}"]))
        prev_answer_idx += 1
    
    # Extract current batch answers
    start_idx = batch_num * 5
    end_idx = min(start_idx + 5, len(KEY_SYMPTOMS))
    
    # Handle back button
    if action == "back":
        # Reconstruct answers from all_ and remove current batch
        all_answers = all_answers[:start_idx]
        return HTMLResponse(render_questions_batch(batch_num - 1, all_answers))
    
    # Get current batch question answers
    for i in range(start_idx, end_idx):
        field_name = f"symptom_{i}"
        if field_name in form_data:
            severity_text = form_data[field_name]
            # Get the numeric score for this severity level
            from logic import get_symptom_options
            options = get_symptom_options(KEY_SYMPTOMS[i])
            score = options.get(severity_text, 0)
            all_answers.append(score)
    
    # Check if all questions answered
    if end_idx >= len(KEY_SYMPTOMS):
        # All questions done - show diagnosis
        diagnosis = diagnose(all_answers)
        return HTMLResponse(render_result(diagnosis))
    
    # Otherwise, show next batch
    next_batch = batch_num + 1
    return HTMLResponse(render_questions_batch(next_batch, all_answers))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)