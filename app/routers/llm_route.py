import logging
from fastapi import APIRouter

from app.models.llm_client import llm_client
from app.schemas.qa import Answer, Question

router = APIRouter()

# Define your LLM-related endpoints here


@router.post("/llm/ask", response_model=Answer)
async def ask_question(question: Question):
    answer = llm_client.ask(question.text)
    logging.info(f"Question: {question.text}, Answer: {answer}")
    # return {"question": question.text, "answer": "This is a dummy answer from the LLM."}
    return Answer(answer=answer)

# def ask_llm(req: QARequest):
#     answer = llm_client.ask(req.question)
#     return QAResponse(answer=answer)