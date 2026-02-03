import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ChromaDBClient:
    def __init__(self):
        self.client = None
        self.collection = None
    
    def connect(self):
        """Connect to ChromaDB"""
        try:
            self.client = chromadb.HttpClient(
                host=settings.chromadb_host,
                port=settings.chromadb_port,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=settings.chromadb_collection_name,
                metadata={"description": "Document embeddings for blog generation"}
            )
            
            logger.info(f"Connected to ChromaDB collection: {settings.chromadb_collection_name}")
        except Exception as e:
            logger.error(f"Could not connect to ChromaDB: {e}")
            raise
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ):
        """Add documents to ChromaDB"""
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            raise
    
    def query_documents(
        self,
        query_texts: List[str],
        n_results: int = 5,
        where: Dict = None
    ):
        """Query documents from ChromaDB"""
        try:
            results = self.collection.query(
                query_texts=query_texts,
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}")
            raise
    
    def delete_documents(self, ids: List[str]):
        """Delete documents from ChromaDB"""
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from ChromaDB")
        except Exception as e:
            logger.error(f"Error deleting documents from ChromaDB: {e}")
            raise
    
    def get_documents_by_user(self, user_id: str):
        """Get all documents for a user"""
        try:
            results = self.collection.get(
                where={"user_id": user_id}
            )
            return results
        except Exception as e:
            logger.error(f"Error getting documents for user: {e}")
            raise


# Global ChromaDB client instance
chroma_client = ChromaDBClient()


def get_chroma_client() -> ChromaDBClient:
    """Get ChromaDB client instance"""
    return chroma_client
