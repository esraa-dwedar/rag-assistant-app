import os
import chromadb
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.utils.logging_config import logger

class RetrievalService:
    def __init__(self):
        self.embed_model = None
        self.collection = None

    def initialize(self):
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL_NAME}")
        self.embed_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        
        # Absolute or relative path resolution
        db_path = settings.CHROMA_PERSIST_DIR
        if not os.path.isabs(db_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(base_dir, db_path)
            
        logger.info(f"Loading ChromaDB from {db_path}")
        client = chromadb.PersistentClient(path=db_path)
        self.collection = client.get_or_create_collection(name="devops_docs")

    def retrieve(self, query: str, top_k: int = 2):
        if not self.embed_model or not self.collection:
            raise RuntimeError("RetrievalService is not initialized.")
        q_emb = self.embed_model.encode([query]).tolist()
        results = self.collection.query(query_embeddings=q_emb, n_results=top_k)
        
        docs = results['documents'][0] if results['documents'] else []
        metas = results['metadatas'][0] if results['metadatas'] else []
        sources = [m.get('source', 'Unknown') for m in metas]
        return docs, sources

retrieval_service = RetrievalService()