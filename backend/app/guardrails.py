"""
AI Gateway Guardrails for Agentic RAG Math Agent

This module implements input and output guardrails to ensure:
1. Input Validation: Reject non-mathematical queries
2. Output Filtering: Prevent harmful or inappropriate content
3. Content Moderation: Ensure responses are educational and appropriate
"""

import logging
import re
from typing import Dict, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationResult(Enum):
    """Validation result status"""
    APPROVED = "approved"
    REJECTED = "rejected"
    WARNING = "warning"


class InputGuardrails:
    """
    Input guardrails to validate incoming queries.
    Ensures queries are math-related and appropriate.
    """
    
    # Math-related keywords (expanded list)
    MATH_KEYWORDS = {
        # Topics
        'calculus', 'algebra', 'geometry', 'trigonometry', 'probability', 
        'statistics', 'arithmetic', 'mathematics', 'math', 'number',
        'equation', 'function', 'variable', 'constant',
        
        # Operations
        'solve', 'evaluate', 'calculate', 'compute', 'find', 'determine',
        'simplify', 'expand', 'factor', 'integrate', 'differentiate', 'derive',
        'prove', 'verify', 'show', 'demonstrate',
        
        # Calculus
        'derivative', 'integral', 'limit', 'series', 'differential',
        'partial', 'gradient', 'optimization', 'convergence',
        
        # Algebra
        'polynomial', 'quadratic', 'cubic', 'linear', 'exponential',
        'logarithm', 'logarithmic', 'radical', 'rational', 'irrational',
        'root', 'solution', 'inequality', 'system',
        
        # Geometry
        'triangle', 'circle', 'rectangle', 'polygon', 'angle', 'area',
        'perimeter', 'volume', 'surface', 'coordinate', 'distance', 'slope',
        
        # Trigonometry
        'sine', 'cosine', 'tangent', 'secant', 'cosecant', 'cotangent',
        'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'radian', 'degree',
        
        # Probability
        'probability', 'permutation', 'combination', 'distribution',
        'random', 'expected', 'variance', 'mean', 'median', 'mode',
        
        # Symbols/Math notation
        'pi', 'sigma', 'theta', 'delta', 'alpha', 'beta', 'gamma',
        'infinity', 'sum', 'product',
        
        # Numbers
        'prime', 'composite', 'fraction', 'decimal', 'integer', 'real',
        'complex', 'imaginary', 'rational'
    }
    
    # Math symbols that indicate mathematical content
    MATH_SYMBOLS = {
        '=', '+', '-', '*', '/', '^', '√', '∫', '∂', '∑', '∏', 'Δ', '∇',
        '≤', '≥', '≠', '≈', '∈', '∉', '⊂', '⊃', '∪', '∩', '∅', '∞',
        'α', 'β', 'γ', 'θ', 'λ', 'μ', 'π', 'σ', 'φ', 'ω',
        '²', '³', '⁴', '⁵', '₁', '₂', '₃'
    }
    
    # Prohibited content indicators
    PROHIBITED_CONTENT = {
        # Off-topic
        'weather', 'recipe', 'movie', 'music', 'sports', 'politics',
        'celebrity', 'news', 'shopping', 'dating', 'social media',
        
        # Harmful
        'hack', 'crack', 'pirate', 'illegal', 'weapon', 'drug',
        'violence', 'harm', 'dangerous', 'explosive',
        
        # Inappropriate
        'adult', 'nsfw', 'explicit', 'profanity'
    }
    
    @classmethod
    def validate_input(cls, question: str) -> Tuple[ValidationResult, str]:
        """
        Validate input question to ensure it's math-related and appropriate.
        
        Args:
            question: User's input question
            
        Returns:
            Tuple of (ValidationResult, message)
        """
        if not question or len(question.strip()) < 5:
            return (
                ValidationResult.REJECTED,
                "Question is too short. Please provide a meaningful math question."
            )
        
        question_lower = question.lower()
        
        # Check for prohibited content
        for prohibited in cls.PROHIBITED_CONTENT:
            if prohibited in question_lower:
                logger.warning(f"Rejected question containing prohibited term: {prohibited}")
                return (
                    ValidationResult.REJECTED,
                    f"This question appears to be off-topic or inappropriate. "
                    f"Please ask a mathematics-related question."
                )
        
        # Check for math keywords
        has_math_keyword = any(
            keyword in question_lower 
            for keyword in cls.MATH_KEYWORDS
        )
        
        # Check for math symbols
        has_math_symbol = any(
            symbol in question 
            for symbol in cls.MATH_SYMBOLS
        )
        
        # Check for numbers (digits)
        has_numbers = bool(re.search(r'\d', question))
        
        # Math expression patterns (e.g., x^2, sin(x), etc.)
        math_patterns = [
            r'[a-zA-Z]\s*[\+\-\*\/\^]\s*\d',  # x+2, y*3, etc.
            r'\d\s*[a-zA-Z]',  # 2x, 3y, etc.
            r'\([a-zA-Z]\)',  # (x), (y), etc.
            r'[a-zA-Z]\^',  # x^, y^, etc.
            r'\\[a-zA-Z]+',  # LaTeX notation
        ]
        has_math_pattern = any(
            re.search(pattern, question) 
            for pattern in math_patterns
        )
        
        # Calculate confidence score
        indicators = {
            'keyword': has_math_keyword,
            'symbol': has_math_symbol,
            'number': has_numbers,
            'pattern': has_math_pattern
        }
        
        confidence = sum(indicators.values()) / len(indicators)
        
        # Decision logic
        if confidence >= 0.5:  # At least 2 out of 4 indicators
            logger.info(f"Input approved with confidence {confidence:.2f}")
            return (
                ValidationResult.APPROVED,
                "Question validated as math-related."
            )
        elif confidence >= 0.25:  # At least 1 indicator
            logger.warning(f"Input borderline with confidence {confidence:.2f}")
            return (
                ValidationResult.WARNING,
                "Question may not be math-related, but will process. "
                "For best results, include mathematical terms or symbols."
            )
        else:
            logger.warning(f"Rejected question with low math relevance: {confidence:.2f}")
            return (
                ValidationResult.REJECTED,
                "This doesn't appear to be a mathematics question. "
                "Please ask about calculus, algebra, geometry, probability, "
                "or other math topics."
            )
    
    @classmethod
    def get_validation_report(cls, question: str) -> Dict:
        """
        Generate detailed validation report for debugging.
        
        Args:
            question: User's input question
            
        Returns:
            Dict with validation details
        """
        question_lower = question.lower()
        
        # Find matched keywords
        matched_keywords = [
            kw for kw in cls.MATH_KEYWORDS 
            if kw in question_lower
        ]
        
        # Find matched symbols
        matched_symbols = [
            sym for sym in cls.MATH_SYMBOLS 
            if sym in question
        ]
        
        # Find prohibited terms
        matched_prohibited = [
            term for term in cls.PROHIBITED_CONTENT 
            if term in question_lower
        ]
        
        result, message = cls.validate_input(question)
        
        return {
            'result': result.value,
            'message': message,
            'question_length': len(question),
            'matched_keywords': matched_keywords[:5],  # Limit to 5
            'matched_symbols': matched_symbols[:5],
            'prohibited_terms': matched_prohibited,
            'has_numbers': bool(re.search(r'\d', question)),
            'total_indicators': len(matched_keywords) + len(matched_symbols)
        }


class OutputGuardrails:
    """
    Output guardrails to filter and validate AI-generated responses.
    Ensures responses are safe, educational, and appropriate.
    """
    
    # Harmful content patterns
    HARMFUL_PATTERNS = [
        r'(?i)(hack|crack|exploit)',  # Security threats
        r'(?i)(weapon|bomb|explosive)',  # Dangerous items
        r'(?i)(drug|narcotic|substance abuse)',  # Illegal substances
        r'(?i)(suicide|self-harm|kill yourself)',  # Self-harm
        r'(?i)(racist|sexist|homophobic)',  # Hate speech
    ]
    
    # Low-quality response indicators
    LOW_QUALITY_PATTERNS = [
        r'^(I don\'t know|I cannot|I\'m unable)',
        r'(?i)(error|failed|could not)',
        r'^$',  # Empty response
    ]
    
    @classmethod
    def validate_output(cls, response: str, question: str = "") -> Tuple[ValidationResult, str]:
        """
        Validate AI-generated response for safety and quality.
        
        Args:
            response: AI-generated response text
            question: Original question (for context)
            
        Returns:
            Tuple of (ValidationResult, message)
        """
        if not response or len(response.strip()) < 10:
            return (
                ValidationResult.REJECTED,
                "Response is too short or empty."
            )
        
        # Check for harmful content
        for pattern in cls.HARMFUL_PATTERNS:
            if re.search(pattern, response):
                logger.error(f"Blocked harmful content in response")
                return (
                    ValidationResult.REJECTED,
                    "Response contains inappropriate or harmful content."
                )
        
        # Check for low-quality responses
        is_low_quality = False
        for pattern in cls.LOW_QUALITY_PATTERNS:
            if re.search(pattern, response):
                is_low_quality = True
                break
        
        if is_low_quality:
            logger.warning("Response flagged as low quality")
            return (
                ValidationResult.WARNING,
                "Response quality is below threshold."
            )
        
        # Check if response seems relevant to math
        math_terms = ['step', 'solve', 'equation', 'answer', 'calculate', 
                     'formula', 'theorem', 'proof', 'solution']
        has_math_content = any(term in response.lower() for term in math_terms)
        
        if not has_math_content and len(response) > 100:
            logger.warning("Response lacks mathematical content")
            return (
                ValidationResult.WARNING,
                "Response may not be math-related."
            )
        
        logger.info("Output validated successfully")
        return (
            ValidationResult.APPROVED,
            "Response validated as safe and appropriate."
        )
    
    @classmethod
    def sanitize_output(cls, response: str) -> str:
        """
        Sanitize response by removing or masking inappropriate content.
        
        Args:
            response: Original response
            
        Returns:
            Sanitized response
        """
        sanitized = response
        
        # Remove potential harmful URLs
        sanitized = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
                          '[URL removed]', sanitized)
        
        # Remove email addresses
        sanitized = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                          '[email removed]', sanitized)
        
        # Remove phone numbers
        sanitized = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', 
                          '[phone removed]', sanitized)
        
        return sanitized


class AIGateway:
    """
    Main AI Gateway class that combines input and output guardrails.
    """
    
    @staticmethod
    def process_query(question: str) -> Dict:
        """
        Process query through input guardrails.
        
        Args:
            question: User's question
            
        Returns:
            Dict with validation result and details
        """
        result, message = InputGuardrails.validate_input(question)
        
        return {
            'approved': result == ValidationResult.APPROVED,
            'result': result.value,
            'message': message,
            'question': question
        }
    
    @staticmethod
    def process_response(response: str, question: str = "") -> Dict:
        """
        Process AI response through output guardrails.
        
        Args:
            response: AI-generated response
            question: Original question
            
        Returns:
            Dict with validation result and sanitized response
        """
        result, message = OutputGuardrails.validate_output(response, question)
        
        # Sanitize if approved or warning
        if result in [ValidationResult.APPROVED, ValidationResult.WARNING]:
            sanitized = OutputGuardrails.sanitize_output(response)
        else:
            sanitized = "Response blocked by safety guardrails."
        
        return {
            'approved': result == ValidationResult.APPROVED,
            'result': result.value,
            'message': message,
            'original_response': response,
            'response': sanitized
        }
    
    @staticmethod
    def get_full_report(question: str, response: str = None) -> Dict:
        """
        Generate comprehensive guardrails report.
        
        Args:
            question: User's question
            response: AI response (optional)
            
        Returns:
            Dict with full validation details
        """
        report = {
            'input': InputGuardrails.get_validation_report(question),
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        
        if response:
            output_result, output_message = OutputGuardrails.validate_output(response, question)
            report['output'] = {
                'result': output_result.value,
                'message': output_message,
                'response_length': len(response),
                'sanitized': output_result != ValidationResult.REJECTED
            }
        
        return report
