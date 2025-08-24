import pytest
from app.services.query_service import QueryService

def test_query_returns_results():
    service = QueryService()
    results = service.query("test query")
    assert isinstance(results, list)
