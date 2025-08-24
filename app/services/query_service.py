from llama_index.vector_stores import SimpleVectorStore
from typing import List

class QueryService:
    def __init__(self, vector_store_path: str = "data/index_store/"):
        self.vector_store = SimpleVectorStore(persist_dir=vector_store_path)

    def query(self, query_text: str, top_k: int = 3) -> List[str]:
        results = self.vector_store.similarity_search(query_text, top_k=top_k)
        return [r["text"] for r in results]
