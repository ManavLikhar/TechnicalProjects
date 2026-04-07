import os
from fastapi import HTTPException
from openai import AsyncOpenAI
from langchain_core.output_parsers import JsonOutputParser
from models.mcq_model import MCQRequest, MCQResponse

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_mcq_paper(request: MCQRequest) -> MCQResponse:
    try:
        parser = JsonOutputParser(pydantic_object=MCQResponse)
        
        prompt = f"""
        Generate {request.num_questions} MCQs.
        {parser.get_format_instructions()}
        """

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        data = parser.parse(response.choices[0].message.content)

        return MCQResponse(**data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))