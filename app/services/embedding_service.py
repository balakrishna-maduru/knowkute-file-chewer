from llama_index.embeddings import SentenceTransformerEmbedding

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformerEmbedding(model_name=model_name)

    def embed_text(self, text: str):
        return self.model.get_text_embedding(text)
