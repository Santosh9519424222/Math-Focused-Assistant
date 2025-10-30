"""
Human-in-the-Loop (HITL) Feedback System with DSPy
Enables users to rate responses and system to learn from feedback
"""

import logging
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import dspy
from enum import Enum

logger = logging.getLogger(__name__)


class FeedbackRating(Enum):
    """Feedback rating options"""
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"


class FeedbackType(Enum):
    """Type of feedback"""
    RATING = "rating"
    CORRECTION = "correction"
    COMMENT = "comment"


class FeedbackStore:
    """
    Storage for user feedback with persistence to JSON file
    """
    
    def __init__(self, storage_path: str = "data/feedback.json"):
        """
        Initialize feedback store
        
        Args:
            storage_path: Path to JSON file for storing feedback
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing feedback
        self.feedback_data = self._load_feedback()
        
        logger.info(f"FeedbackStore initialized with {len(self.feedback_data)} existing entries")
    
    def _load_feedback(self) -> List[Dict]:
        """Load feedback from JSON file"""
        if not self.storage_path.exists():
            return []
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading feedback: {e}")
            return []
    
    def _save_feedback(self):
        """Save feedback to JSON file"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.feedback_data)} feedback entries")
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
    
    def add_feedback(
        self,
        question: str,
        answer: str,
        rating: str,
        feedback_type: str = "rating",
        correction: str = None,
        comment: str = None,
        metadata: Dict = None
    ) -> Dict:
        """
        Add new feedback entry
        
        Args:
            question: Original user question
            answer: System's answer
            rating: User rating (thumbs_up/thumbs_down)
            feedback_type: Type of feedback
            correction: User's correction (optional)
            comment: User's comment (optional)
            metadata: Additional metadata (source, confidence, etc.)
            
        Returns:
            Feedback entry with generated ID
        """
        feedback_entry = {
            "id": len(self.feedback_data) + 1,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "rating": rating,
            "feedback_type": feedback_type,
            "correction": correction,
            "comment": comment,
            "metadata": metadata or {}
        }
        
        self.feedback_data.append(feedback_entry)
        self._save_feedback()
        
        logger.info(f"Added feedback #{feedback_entry['id']}: {rating}")
        return feedback_entry
    
    def get_feedback_by_rating(self, rating: str) -> List[Dict]:
        """Get all feedback entries with specific rating"""
        return [fb for fb in self.feedback_data if fb['rating'] == rating]
    
    def get_positive_feedback(self) -> List[Dict]:
        """Get all positive feedback (thumbs up)"""
        return self.get_feedback_by_rating(FeedbackRating.THUMBS_UP.value)
    
    def get_negative_feedback(self) -> List[Dict]:
        """Get all negative feedback (thumbs down)"""
        return self.get_feedback_by_rating(FeedbackRating.THUMBS_DOWN.value)
    
    def get_feedback_with_corrections(self) -> List[Dict]:
        """Get feedback entries that include corrections"""
        return [fb for fb in self.feedback_data if fb.get('correction')]
    
    def get_statistics(self) -> Dict:
        """Get feedback statistics"""
        total = len(self.feedback_data)
        positive = len(self.get_positive_feedback())
        negative = len(self.get_negative_feedback())
        with_corrections = len(self.get_feedback_with_corrections())
        
        return {
            "total_feedback": total,
            "positive": positive,
            "negative": negative,
            "positive_rate": positive / total if total > 0 else 0,
            "negative_rate": negative / total if total > 0 else 0,
            "with_corrections": with_corrections,
            "correction_rate": with_corrections / total if total > 0 else 0
        }


class DSPyOptimizer:
    """
    DSPy-based optimizer for learning from feedback
    Uses feedback to improve system responses
    """
    
    def __init__(self, feedback_store: FeedbackStore):
        """
        Initialize DSPy optimizer
        
        Args:
            feedback_store: Feedback store instance
        """
        self.feedback_store = feedback_store
        
        # Initialize DSPy (we'll use it for prompt optimization)
        # For now, we'll use a simple approach without external LM
        logger.info("DSPy optimizer initialized")
    
    def analyze_negative_feedback(self) -> Dict:
        """
        Analyze negative feedback to find patterns
        
        Returns:
            Analysis with common issues and recommendations
        """
        negative_feedback = self.feedback_store.get_negative_feedback()
        
        if not negative_feedback:
            return {
                "total_negative": 0,
                "issues": [],
                "recommendations": []
            }
        
        # Analyze patterns in negative feedback
        issues = []
        sources = {}
        topics = {}
        
        for fb in negative_feedback:
            # Count by source
            source = fb.get('metadata', {}).get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
            
            # Extract topics from questions
            question_lower = fb['question'].lower()
            for topic in ['calculus', 'algebra', 'geometry', 'probability', 'trigonometry']:
                if topic in question_lower:
                    topics[topic] = topics.get(topic, 0) + 1
        
        # Generate recommendations
        recommendations = []
        
        # Source-based recommendations
        if sources.get('perplexity_web', 0) > sources.get('gemini_with_db', 0):
            recommendations.append({
                "type": "expand_knowledge_base",
                "priority": "high",
                "reason": "More negative feedback from web search than DB matches",
                "action": "Add more problems to knowledge base"
            })
        
        if sources.get('not_found', 0) > 0:
            recommendations.append({
                "type": "improve_search",
                "priority": "high",
                "reason": f"{sources.get('not_found', 0)} queries not answered",
                "action": "Improve semantic search or lower confidence threshold"
            })
        
        # Topic-based recommendations
        for topic, count in sorted(topics.items(), key=lambda x: x[1], reverse=True):
            if count >= 2:
                recommendations.append({
                    "type": "topic_coverage",
                    "priority": "medium",
                    "reason": f"{count} negative feedback for {topic} questions",
                    "action": f"Add more {topic} problems to knowledge base"
                })
        
        return {
            "total_negative": len(negative_feedback),
            "sources": sources,
            "topics": topics,
            "recommendations": recommendations[:5]  # Top 5
        }
    
    def generate_training_examples(self) -> List[Dict]:
        """
        Generate training examples from positive feedback
        These can be used for DSPy optimization
        
        Returns:
            List of training examples
        """
        positive_feedback = self.feedback_store.get_positive_feedback()
        
        training_examples = []
        for fb in positive_feedback:
            example = {
                "question": fb['question'],
                "answer": fb['answer'],
                "metadata": fb.get('metadata', {}),
                "rating": "positive"
            }
            training_examples.append(example)
        
        logger.info(f"Generated {len(training_examples)} training examples from positive feedback")
        return training_examples
    
    def suggest_improvements(self) -> Dict:
        """
        Suggest improvements based on all feedback
        
        Returns:
            Comprehensive improvement suggestions
        """
        stats = self.feedback_store.get_statistics()
        negative_analysis = self.analyze_negative_feedback()
        
        suggestions = {
            "overall_performance": {
                "positive_rate": f"{stats['positive_rate']:.1%}",
                "total_feedback": stats['total_feedback'],
                "status": "good" if stats['positive_rate'] >= 0.7 else "needs_improvement"
            },
            "priority_actions": negative_analysis['recommendations'],
            "next_steps": []
        }
        
        # Add specific next steps
        if stats['total_feedback'] < 10:
            suggestions['next_steps'].append({
                "action": "collect_more_feedback",
                "reason": "Insufficient data for meaningful optimization"
            })
        
        if stats['positive_rate'] < 0.6:
            suggestions['next_steps'].append({
                "action": "review_negative_feedback",
                "reason": f"Low positive rate ({stats['positive_rate']:.1%})"
            })
        
        if stats['with_corrections'] > 0:
            suggestions['next_steps'].append({
                "action": "incorporate_corrections",
                "reason": f"{stats['with_corrections']} users provided corrections"
            })
        
        return suggestions


class HITLFeedbackSystem:
    """
    Main Human-in-the-Loop Feedback System
    Combines feedback collection and DSPy optimization
    """
    
    def __init__(self, storage_path: str = "data/feedback.json"):
        """Initialize HITL system"""
        self.feedback_store = FeedbackStore(storage_path)
        self.optimizer = DSPyOptimizer(self.feedback_store)
        
        logger.info("HITL Feedback System initialized")
    
    def submit_feedback(
        self,
        question: str,
        answer: str,
        rating: str,
        correction: str = None,
        comment: str = None,
        metadata: Dict = None
    ) -> Dict:
        """
        Submit user feedback
        
        Args:
            question: Original question
            answer: System answer
            rating: thumbs_up or thumbs_down
            correction: User's correction (optional)
            comment: User's comment (optional)
            metadata: Additional context
            
        Returns:
            Feedback confirmation
        """
        # Validate rating
        try:
            FeedbackRating(rating)
        except ValueError:
            raise ValueError(f"Invalid rating: {rating}. Must be 'thumbs_up' or 'thumbs_down'")
        
        # Determine feedback type
        if correction:
            feedback_type = FeedbackType.CORRECTION.value
        elif comment:
            feedback_type = FeedbackType.COMMENT.value
        else:
            feedback_type = FeedbackType.RATING.value
        
        # Add to store
        entry = self.feedback_store.add_feedback(
            question=question,
            answer=answer,
            rating=rating,
            feedback_type=feedback_type,
            correction=correction,
            comment=comment,
            metadata=metadata
        )
        
        # Trigger learning if enough feedback
        if len(self.feedback_store.feedback_data) % 10 == 0:
            logger.info("Triggering optimization analysis...")
            suggestions = self.optimizer.suggest_improvements()
            logger.info(f"Optimization suggestions: {suggestions['priority_actions']}")
        
        return {
            "success": True,
            "feedback_id": entry['id'],
            "message": "Thank you for your feedback! This helps improve the system.",
            "timestamp": entry['timestamp']
        }
    
    def get_statistics(self) -> Dict:
        """Get feedback statistics"""
        return self.feedback_store.get_statistics()
    
    def get_improvements(self) -> Dict:
        """Get improvement suggestions"""
        return self.optimizer.suggest_improvements()
    
    def get_learning_report(self) -> Dict:
        """
        Generate comprehensive learning report
        
        Returns:
            Detailed report with stats and recommendations
        """
        stats = self.get_statistics()
        improvements = self.get_improvements()
        negative_analysis = self.optimizer.analyze_negative_feedback()
        
        return {
            "statistics": stats,
            "negative_feedback_analysis": {
                "total": negative_analysis['total_negative'],
                "by_source": negative_analysis['sources'],
                "by_topic": negative_analysis['topics']
            },
            "improvements": improvements,
            "timestamp": datetime.now().isoformat()
        }


# Global HITL system instance
hitl_system = None


def get_hitl_system() -> HITLFeedbackSystem:
    """Get or create global HITL system instance"""
    global hitl_system
    if hitl_system is None:
        # Create data directory in backend folder
        storage_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "feedback.json"
        )
        hitl_system = HITLFeedbackSystem(storage_path)
    return hitl_system
