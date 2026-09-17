import ollama
from app.core.config import settings
from app.utils.logging_config import logger

class GenerationService:
    def __init__(self):
        self.client = None

    def initialize(self):
        logger.info(f"Connecting to Ollama at {settings.OLLAMA_BASE_URL}")
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)

    def generate_answer(self, question: str, contexts: list[str], sources: list[str]) -> str:
        if not contexts:
            return "I could not find relevant documentation to answer this question."
            
        context_block = "\n---\n".join([f"Source [{s}]: {c}" for c, s in zip(contexts, sources)])
        prompt = f"""You are a reliable DevOps technical assistant. 
Use strictly the provided context below to answer the user query.
If the information is not in the context, explicitly respond: "I cannot find the answer in the provided documents."
Cite the document sources in your answer.

Context:
{context_block}

User Question: {question}
Answer:"""

        try:
            response = self.client.chat(
                model=settings.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1}
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return f"Error contacting language model: {str(e)}"

generation_service = GenerationService()