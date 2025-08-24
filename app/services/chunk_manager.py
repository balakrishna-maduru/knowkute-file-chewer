from typing import List
import re

class ChunkManager:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def create_chunks(self, text: str) -> List[str]:
        # Split text into sentences (simple split, can be improved)
        sentences = re.split(r'(?<=[.!?]) +', text)
        chunks = []
        current_chunk = []
        current_length = 0
        for sentence in sentences:
            if current_length + len(sentence) > self.chunk_size:
                chunks.append(' '.join(current_chunk))
                # Overlap
                current_chunk = current_chunk[-self.overlap:] if self.overlap else []
                current_length = sum(len(s) for s in current_chunk)
            current_chunk.append(sentence)
            current_length += len(sentence)
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return [c for c in chunks if c.strip()]
