from pydantic import BaseModel, Field
from typing import List

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, description="The user query")

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]