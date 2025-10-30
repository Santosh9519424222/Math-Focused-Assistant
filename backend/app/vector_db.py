"""
Vector Database module using Qdrant for storing and retrieving math problems.
Uses sentence-transformers for local embeddings (no API key needed).
"""

import logging
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import os

logger = logging.getLogger(__name__)


class MathKnowledgeBase:
    """Knowledge Base for math problems using Qdrant vector database."""
    
    def __init__(self, collection_name: str = "math_problems"):
        """Initialize Qdrant client and create collection if needed."""
        self.collection_name = collection_name
        
        # Initialize Qdrant client (in-memory for development)
        self.client = QdrantClient(":memory:")
        logger.info("Initialized Qdrant client (in-memory mode)")
        
        # Initialize sentence-transformers for local embeddings (no API key needed!)
        logger.info("Loading sentence-transformers model (this may take a moment on first run)...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        
        # Create collection if it doesn't exist
        self._create_collection()
        
    def _create_collection(self):
        """Create Qdrant collection with proper schema."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence-transformers (local, no API needed)."""
        try:
            # Generate embedding locally
            embedding = self.embedding_model.encode(text, convert_to_tensor=False)
            # Convert numpy array to list
            embedding_list = embedding.tolist()
            logger.debug(f"Generated embedding for text: {text[:50]}...")
            return embedding_list
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def add_problem(
        self,
        problem_id: str,
        question: str,
        solution_steps: List[str],
        final_answer: str,
        difficulty: str,
        tags: List[str],
        topic: str
    ):
        """Add a math problem to the knowledge base."""
        try:
            # Generate embedding for the question
            embedding = self.generate_embedding(question)
            
            # Convert string ID to integer hash (Qdrant accepts int or UUID)
            import hashlib
            point_id = int(hashlib.md5(problem_id.encode()).hexdigest()[:8], 16)
            
            # Create point with metadata
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "problem_id": problem_id,  # Store original ID in payload
                    "question": question,
                    "solution_steps": solution_steps,
                    "final_answer": final_answer,
                    "difficulty": difficulty,
                    "tags": tags,
                    "topic": topic
                }
            )
            
            # Upsert to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            logger.info(f"Added problem: {problem_id}")
            
        except Exception as e:
            logger.error(f"Error adding problem: {e}")
            raise
    
    def search_similar(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.7,
        topic_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for similar problems in the knowledge base.
        
        Args:
            query: The question to search for
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)
            topic_filter: Optional topic filter
            
        Returns:
            List of search results with metadata and confidence scores
        """
        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query)
            
            # Build filter if topic specified
            search_filter = None
            if topic_filter:
                search_filter = Filter(
                    must=[
                        FieldCondition(
                            key="topic",
                            match=MatchValue(value=topic_filter)
                        )
                    ]
                )
            
            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=score_threshold,
                query_filter=search_filter
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "problem_id": result.payload.get("problem_id"),
                    "score": result.score,
                    "question": result.payload.get("question"),
                    "solution_steps": result.payload.get("solution_steps"),
                    "final_answer": result.payload.get("final_answer"),
                    "difficulty": result.payload.get("difficulty"),
                    "tags": result.payload.get("tags"),
                    "topic": result.payload.get("topic")
                })
            
            logger.info(f"Found {len(results)} similar problems for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    def get_retrieval_confidence(self, search_results: List[Dict]) -> tuple[str, float]:
        """
        Determine retrieval confidence level based on search results.
        
        Returns:
            Tuple of (confidence_level, best_score)
            confidence_level: "high", "medium", "low", "none"
        """
        if not search_results:
            return "none", 0.0
        
        best_score = search_results[0]["score"]
        return self.get_confidence_from_score(best_score), best_score
    
    def get_confidence_from_score(self, score: float) -> str:
        """
        Get confidence level from a similarity score.
        
        Args:
            score: Similarity score (0-1)
            
        Returns:
            Confidence level: "high", "medium", "low", or "none"
        """
        if score >= 0.85:
            return "high"
        elif score >= 0.70:
            return "medium"
        elif score >= 0.50:
            return "low"
        else:
            return "none"
    
    def count_problems(self) -> int:
        """Count total number of problems in KB."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            logger.error(f"Error counting problems: {e}")
            return 0
