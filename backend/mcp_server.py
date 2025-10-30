"""
MCP Server for Agentic RAG Math Agent
Exposes math knowledge base search and retrieval via Model Context Protocol

This MCP server provides three main tools:
1. search_math_problems - Search for similar problems in the knowledge base
2. get_problem_details - Get complete details of a specific problem
3. list_topics - List all available topics in the knowledge base
"""

from typing import Any
from mcp.server.fastmcp import FastMCP
import sys
import os
import logging

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.vector_db import MathKnowledgeBase

# Configure logging to stderr (NOT stdout - would break MCP protocol!)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # IMPORTANT: MCP servers must NOT write to stdout
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("math-agent")

# Initialize knowledge base
kb = None

def initialize_kb():
    """Initialize and populate the knowledge base"""
    global kb
    
    logger.info("Initializing Math Knowledge Base for MCP...")
    kb = MathKnowledgeBase()
    
    # Populate with sample problems
    sample_problems = [
        {
            "problem_id": "calc_001",
            "question": "Evaluate the integral ∫₀¹ x² ln(x) dx using integration by parts",
            "solution_steps": [
                "Use integration by parts with u = ln(x) and dv = x² dx",
                "Then du = (1/x)dx and v = x³/3",
                "Apply the formula: ∫u dv = uv - ∫v du",
                "This gives: [x³ln(x)/3]₀¹ - ∫₀¹ (x³/3)(1/x) dx",
                "Simplify: [x³ln(x)/3]₀¹ - ∫₀¹ x²/3 dx",
                "Evaluate limits and integral: 0 - [x³/9]₀¹ = -1/9"
            ],
            "final_answer": "-1/9",
            "difficulty": "JEE_Advanced",
            "tags": ["integration", "integration_by_parts", "logarithm"],
            "topic": "Calculus"
        },
        {
            "problem_id": "alg_001",
            "question": "Solve for x: x³ - 3x + 2 = 0",
            "solution_steps": [
                "Try to factor the cubic equation",
                "Test x = 1: 1³ - 3(1) + 2 = 0 ✓",
                "So (x - 1) is a factor",
                "Perform polynomial division: (x³ - 3x + 2) ÷ (x - 1) = x² + x - 2",
                "Factor the quadratic: x² + x - 2 = (x + 2)(x - 1)",
                "Therefore: (x - 1)(x + 2)(x - 1) = (x - 1)²(x + 2) = 0",
                "Solutions: x = 1 (double root) and x = -2"
            ],
            "final_answer": "x = 1 (multiplicity 2), x = -2",
            "difficulty": "JEE_Main",
            "tags": ["polynomial", "cubic_equation", "factorization"],
            "topic": "Algebra"
        },
        {
            "problem_id": "calc_004",
            "question": "Find the derivative of f(x) = x^x for x > 0",
            "solution_steps": [
                "Take natural logarithm of both sides: ln(f(x)) = ln(x^x) = x ln(x)",
                "Differentiate both sides using implicit differentiation",
                "Left side: (1/f(x)) · f'(x)",
                "Right side: d/dx[x ln(x)] = ln(x) + x·(1/x) = ln(x) + 1",
                "So: f'(x)/f(x) = ln(x) + 1",
                "Therefore: f'(x) = f(x) · (ln(x) + 1) = x^x · (ln(x) + 1)"
            ],
            "final_answer": "f'(x) = x^x(ln(x) + 1)",
            "difficulty": "JEE_Advanced",
            "tags": ["differentiation", "logarithmic_differentiation", "exponential"],
            "topic": "Calculus"
        },
        {
            "problem_id": "prob_001",
            "question": "A box contains 5 red balls and 3 blue balls. If 3 balls are drawn at random without replacement, what is the probability that exactly 2 are red?",
            "solution_steps": [
                "Total balls = 5 + 3 = 8",
                "Need to find P(exactly 2 red in 3 draws)",
                "This means 2 red and 1 blue",
                "Number of ways to choose 2 red from 5: C(5,2) = 10",
                "Number of ways to choose 1 blue from 3: C(3,1) = 3",
                "Number of ways to choose 3 from 8: C(8,3) = 56",
                "P(2 red, 1 blue) = [C(5,2) × C(3,1)] / C(8,3) = (10 × 3) / 56 = 30/56 = 15/28"
            ],
            "final_answer": "15/28 ≈ 0.536",
            "difficulty": "JEE_Main",
            "tags": ["probability", "combinations", "without_replacement"],
            "topic": "Probability"
        },
        {
            "problem_id": "trig_001",
            "question": "Find the Maclaurin series for sin(x) up to the x⁵ term",
            "solution_steps": [
                "Recall the Maclaurin series: f(x) = Σ[f⁽ⁿ⁾(0)/n!]xⁿ",
                "Find derivatives at x=0:",
                "  f(x) = sin(x), f(0) = 0",
                "  f'(x) = cos(x), f'(0) = 1",
                "  f''(x) = -sin(x), f''(0) = 0",
                "  f'''(x) = -cos(x), f'''(0) = -1",
                "  f⁽⁴⁾(x) = sin(x), f⁽⁴⁾(0) = 0",
                "  f⁽⁵⁾(x) = cos(x), f⁽⁵⁾(0) = 1",
                "Substitute into formula:",
                "sin(x) = 0 + x - 0 - x³/3! + 0 + x⁵/5! + ...",
                "sin(x) = x - x³/6 + x⁵/120 + ..."
            ],
            "final_answer": "sin(x) ≈ x - x³/6 + x⁵/120",
            "difficulty": "JEE_Advanced",
            "tags": ["series", "maclaurin_series", "trigonometry"],
            "topic": "Calculus"
        }
    ]
    
    for problem in sample_problems:
        try:
            kb.add_problem(**problem)
            logger.info(f"Added problem: {problem['problem_id']}")
        except Exception as e:
            logger.error(f"Failed to add problem {problem['problem_id']}: {e}")
    
    total = kb.count_problems()
    logger.info(f"Knowledge base initialized with {total} problems")


@mcp.tool()
async def search_math_problems(
    query: str,
    top_k: int = 3,
    score_threshold: float = 0.5,
    topic: str | None = None
) -> str:
    """
    Search for similar math problems in the knowledge base using semantic search.
    
    This tool performs semantic similarity matching to find problems related to the query.
    It returns a list of matching problems with their similarity scores and metadata.
    
    Args:
        query: The math question or problem description to search for
        top_k: Maximum number of results to return (default: 3, max: 10)
        score_threshold: Minimum similarity score from 0.0 to 1.0 (default: 0.5)
        topic: Optional filter by topic (e.g., "Calculus", "Algebra", "Probability")
    
    Returns:
        Formatted string with matching problems, scores, and metadata
    
    Examples:
        - "Find problems about integration by parts"
        - "Search for cubic equation problems"
        - "Show me probability problems about balls"
    """
    logger.info(f"MCP Tool Called: search_math_problems(query={query}, top_k={top_k}, topic={topic})")
    
    if kb is None:
        return "ERROR: Knowledge base not initialized"
    
    try:
        # Validate parameters
        top_k = min(max(1, top_k), 10)  # Limit to 1-10
        score_threshold = max(0.0, min(1.0, score_threshold))  # Limit to 0-1
        
        # Search knowledge base
        results = kb.search_similar(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold,
            topic_filter=topic
        )
        
        if not results:
            return f"No problems found matching '{query}' with score >= {score_threshold}"
        
        # Format results
        output = []
        output.append(f"Found {len(results)} matching problem(s):\n")
        
        for i, result in enumerate(results, 1):
            confidence = kb.get_confidence_from_score(result['score'])
            output.append(f"\n{'='*60}")
            output.append(f"Result #{i}: {result['problem_id']}")
            output.append(f"{'='*60}")
            output.append(f"Similarity Score: {result['score']:.4f} ({confidence.upper()})")
            output.append(f"Topic: {result['topic']}")
            output.append(f"Difficulty: {result['difficulty']}")
            output.append(f"\nQuestion:")
            output.append(f"{result['question']}")
            output.append(f"\nFinal Answer: {result['final_answer']}")
            output.append(f"Tags: {', '.join(result['tags'])}")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"Error in search_math_problems: {e}")
        return f"ERROR: {str(e)}"


@mcp.tool()
async def get_problem_details(problem_id: str) -> str:
    """
    Get complete details of a specific math problem including step-by-step solution.
    
    This tool retrieves a problem by its ID and returns all available information
    including the question, full solution steps, final answer, and metadata.
    
    Args:
        problem_id: The unique identifier of the problem (e.g., "calc_001", "alg_001")
    
    Returns:
        Formatted string with complete problem details and solution steps
    
    Examples:
        - "calc_001" - Get integration by parts problem
        - "alg_001" - Get cubic equation problem
        - "prob_001" - Get probability problem
    """
    logger.info(f"MCP Tool Called: get_problem_details(problem_id={problem_id})")
    
    if kb is None:
        return "ERROR: Knowledge base not initialized"
    
    try:
        # Search for exact match by problem_id
        # We'll search using the problem_id as query with high top_k
        results = kb.search_similar(query=problem_id, top_k=10, score_threshold=0.0)
        
        # Find the exact problem_id match
        problem = None
        for result in results:
            if result['problem_id'] == problem_id:
                problem = result
                break
        
        if not problem:
            available_ids = ", ".join([r['problem_id'] for r in results[:5]])
            return f"Problem '{problem_id}' not found. Available problems: {available_ids}"
        
        # Format complete problem details
        output = []
        output.append(f"{'='*70}")
        output.append(f"PROBLEM: {problem['problem_id']}")
        output.append(f"{'='*70}\n")
        
        output.append(f"📊 Metadata:")
        output.append(f"  Topic: {problem['topic']}")
        output.append(f"  Difficulty: {problem['difficulty']}")
        output.append(f"  Tags: {', '.join(problem['tags'])}\n")
        
        output.append(f"❓ Question:")
        output.append(f"{problem['question']}\n")
        
        if problem['solution_steps']:
            output.append(f"📝 Step-by-Step Solution:")
            for i, step in enumerate(problem['solution_steps'], 1):
                output.append(f"  {i}. {step}")
            output.append("")
        
        output.append(f"✅ Final Answer:")
        output.append(f"  {problem['final_answer']}")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"Error in get_problem_details: {e}")
        return f"ERROR: {str(e)}"


@mcp.tool()
async def list_topics() -> str:
    """
    List all available topics in the knowledge base with problem counts.
    
    This tool provides an overview of what types of math problems are available
    and how many problems exist for each topic.
    
    Returns:
        Formatted list of topics with problem counts and examples
    
    Examples:
        - Use this to discover what topics are available
        - Check which areas have the most coverage
    """
    logger.info(f"MCP Tool Called: list_topics()")
    
    if kb is None:
        return "ERROR: Knowledge base not initialized"
    
    try:
        # Get all problems by searching with empty query
        all_results = kb.search_similar(query="mathematics", top_k=100, score_threshold=0.0)
        
        if not all_results:
            return "No problems found in knowledge base"
        
        # Count problems by topic
        topic_counts = {}
        topic_examples = {}
        
        for result in all_results:
            topic = result['topic']
            if topic not in topic_counts:
                topic_counts[topic] = 0
                topic_examples[topic] = []
            
            topic_counts[topic] += 1
            if len(topic_examples[topic]) < 2:  # Store up to 2 examples
                topic_examples[topic].append(result['problem_id'])
        
        # Format output
        output = []
        output.append(f"{'='*70}")
        output.append(f"KNOWLEDGE BASE TOPICS")
        output.append(f"{'='*70}\n")
        output.append(f"Total Problems: {len(all_results)}\n")
        
        for topic in sorted(topic_counts.keys()):
            count = topic_counts[topic]
            examples = ", ".join(topic_examples[topic])
            output.append(f"📚 {topic}")
            output.append(f"   Problems: {count}")
            output.append(f"   Examples: {examples}\n")
        
        output.append(f"{'='*70}")
        output.append(f"Use search_math_problems() to find specific problems")
        output.append(f"Use get_problem_details() to see full solutions")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"Error in list_topics: {e}")
        return f"ERROR: {str(e)}"


def main():
    """Main entry point for MCP server"""
    logger.info("Starting Math Agent MCP Server...")
    
    # Initialize knowledge base
    initialize_kb()
    
    logger.info("MCP Server ready! Listening for tool calls...")
    
    # Run the MCP server with stdio transport
    # This allows it to communicate with MCP clients like Claude Desktop
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
