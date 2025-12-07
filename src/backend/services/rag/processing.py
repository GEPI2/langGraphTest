import os
from typing import List
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        # Use a lightweight local model for embeddings
        self.embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    def load_document(self, file_path: str) -> List[Document]:
        """Loads a document based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        elif ext == ".pdf":
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return loader.load()

    def process_document(self, file_path: str) -> List[Document]:
        """Loads and splits a document."""
        docs = self.load_document(file_path)
        chunks = self.text_splitter.split_documents(docs)
        return chunks

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of texts."""
        return self.embedding_model.embed_documents(texts)
