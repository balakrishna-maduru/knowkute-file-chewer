from fastapi import APIRouter
from pydantic import BaseModel
from app.services.query_service import QueryService

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/query")
def query_endpoint(request: QueryRequest):
    service = QueryService()
    results = service.query(request.query, top_k=request.top_k)
    return {"results": results}
