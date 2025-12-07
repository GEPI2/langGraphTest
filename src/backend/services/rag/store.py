import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from langchain_core.documents import Document
from src.backend.services.rag.processing import DocumentProcessor
import uuid

class VectorStore:
    def __init__(self, persist_directory: str = "data/chroma"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="rag_collection")
        self.processor = DocumentProcessor()

    def add_documents(self, file_path: str):
        """Processes and adds a document to the vector store."""
        chunks = self.processor.process_document(file_path)
        
        ids = [str(uuid.uuid4()) for _ in chunks]
        documents = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # Embeddings are handled automatically by Chroma if not provided, 
        # but we can use our processor's model if we want consistency outside Chroma.
        # For simplicity, let's let Chroma use its default (all-MiniLM-L6-v2) or pass explicit embeddings.
        # Since we initialized SentenceTransformer in processor, let's use it.
        embeddings = self.processor.get_embeddings(documents)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        return len(chunks)

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Queries the vector store."""
        query_embedding = self.processor.get_embeddings([query_text])
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                })
        
        return formatted_results
