import pytest
from app.services.embedding_service import EmbeddingService

def test_embedding_shape():
    service = EmbeddingService()
    embedding = service.embed_text("test sentence")
    assert isinstance(embedding, list)
    assert len(embedding) > 0
