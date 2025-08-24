import pytest
from app.services.chunk_manager import ChunkManager

@pytest.mark.parametrize("text,expected_chunks", [
    ("Sentence one. Sentence two. Sentence three.", 3),
    ("Short. Another short.", 2)
])
def test_chunking(text, expected_chunks):
    manager = ChunkManager(chunk_size=1)
    chunks = manager.create_chunks(text)
    assert len(chunks) == expected_chunks
