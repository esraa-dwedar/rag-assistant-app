from fastapi import APIRouter, HTTPException
from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import retrieval_service
from app.services.generation import generation_service
from app.utils.logging_config import logger

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "RAG Backend"}

@router.post("/query", response_model=QueryResponse)
def query_documents(payload: QueryRequest):
    try:
        contexts, sources = retrieval_service.retrieve(payload.question, top_k=2)
        answer = generation_service.generate_answer(payload.question, contexts, sources)
        unique_sources = sorted(list(set(sources)))
        return QueryResponse(answer=answer, sources=unique_sources)
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(status_status=500, detail=str(e))