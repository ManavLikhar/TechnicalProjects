from pydantic import BaseModel
from typing import List

class MCQRequest(BaseModel):
    num_questions: int

class MCQ(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class MCQResponse(BaseModel):
    questions: List[MCQ]