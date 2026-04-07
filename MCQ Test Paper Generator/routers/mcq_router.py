from fastapi import APIRouter
from models.mcq_model import MCQRequest, MCQResponse
from controllers.mcq_controller import generate_mcq_paper

mcq_router = APIRouter()

@mcq_router.post("/generate-mcqs", response_model=MCQResponse)
async def create_mcq_test(request: MCQRequest):
    return await generate_mcq_paper(request)