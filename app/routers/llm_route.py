from fastapi import APIRouter

from models.qa import Question

router = APIRouter()

# Define your LLM-related endpoints here


@router.post("/llm/ask")
async def ask_question(question: Question):
    # Dummy response for example
    return {"question": question.text, "answer": "This is a dummy answer from the LLM."}
