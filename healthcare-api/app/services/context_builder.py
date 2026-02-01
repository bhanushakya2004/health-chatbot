import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from agno.models.google import Gemini


class ContextBuilderService:
    """Service for building context-aware prompts using RAG"""
    
    _client = None
    _collection = None
    _embedding_model = None
    
    @classmethod
    def initialize(cls):
        """Initialize ChromaDB client and collection"""
        if cls._client is None:
            # Initialize ChromaDB in persistent mode
            data_path = os.path.join(os.getcwd(), "data", "chromadb")
            os.makedirs(data_path, exist_ok=True)
            
            cls._client = chromadb.PersistentClient(path=data_path)
            
            # Get or create collection
            cls._collection = cls._client.get_or_create_collection(
                name="medical_documents",
                metadata={"description": "Medical documents and reports"}
            )
        
        return cls._collection
    
    @classmethod
    def add_document(cls, document_id: str, text: str, metadata: Dict):
        """
        Add document to vector store
        
        Args:
            document_id: Unique document identifier
            text: Document text content
            metadata: Document metadata (filename, user_id, etc.)
        """
        collection = cls.initialize()
        
        # Split text into chunks (simple chunking by sentences)
        chunks = cls._chunk_text(text, chunk_size=500)
        
        # Add chunks to collection
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{**metadata, "chunk_index": i}],
                ids=[f"{document_id}_chunk_{i}"]
            )
    
    @classmethod
    def _chunk_text(cls, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks for embedding"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    @classmethod
    def search_relevant_documents(cls, query: str, user_id: str, n_results: int = 3) -> List[Dict]:
        """
        Search for relevant document chunks
        
        Args:
            query: Search query
            user_id: User ID to filter results
            n_results: Number of results to return
        
        Returns:
            List of relevant document chunks with metadata
        """
        collection = cls.initialize()
        
        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"user_id": user_id}
            )
            
            if not results or not results['documents']:
                return []
            
            # Format results
            relevant_docs = []
            for i in range(len(results['documents'][0])):
                relevant_docs.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
            
            return relevant_docs
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    @classmethod
    def build_context_prompt(cls, user_query: str, user_id: str, health_summary: Optional[str] = None) -> str:
        """
        Build context-aware prompt for agent
        
        Args:
            user_query: User's current question
            user_id: User identifier
            health_summary: User's health summary
        
        Returns:
            Enhanced prompt with context
        """
        context_parts = []
        
        # Add health summary if available
        if health_summary:
            context_parts.append(f"## Patient Health Summary:\n{health_summary}\n")
        
        # Search for relevant documents
        relevant_docs = cls.search_relevant_documents(user_query, user_id, n_results=3)
        
        if relevant_docs:
            context_parts.append("## Relevant Medical Records:")
            for i, doc in enumerate(relevant_docs, 1):
                filename = doc['metadata'].get('filename', 'Unknown')
                content = doc['content'][:300]  # Limit content length
                context_parts.append(f"{i}. From {filename}:\n{content}...\n")
        
        # Build final prompt
        if context_parts:
            context = "\n".join(context_parts)
            full_prompt = f"""{context}

## Patient Question:
{user_query}

Please answer considering the patient's health history and medical records above."""
            return full_prompt
        else:
            return user_query
    
    @classmethod
    def delete_user_documents(cls, user_id: str):
        """Delete all documents for a user"""
        collection = cls.initialize()
        
        try:
            # Get all document IDs for user
            results = collection.get(where={"user_id": user_id})
            
            if results and results['ids']:
                collection.delete(ids=results['ids'])
                print(f"Deleted {len(results['ids'])} document chunks for user {user_id}")
        except Exception as e:
            print(f"Error deleting user documents: {e}")
