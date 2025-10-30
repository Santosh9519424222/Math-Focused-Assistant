"""
Test script to populate KB and test various queries
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.vector_db import MathKnowledgeBase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize KB
kb = MathKnowledgeBase()

# Add a few sample problems
problems = [
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

print("\n" + "=" * 80)
print("POPULATING KNOWLEDGE BASE")
print("=" * 80)

for problem in problems:
    kb.add_problem(**problem)
    print(f"✓ Added: {problem['problem_id']}")

total = kb.count_problems()
print(f"\n✓ Total problems in KB: {total}\n")

# Test queries
print("=" * 80)
print("TESTING QUERIES")
print("=" * 80)

test_cases = [
    {
        "name": "Test 1: Exact match - Integration by parts",
        "query": "How to evaluate integral of x squared times log x?",
        "expected": "calc_001"
    },
    {
        "name": "Test 2: Similar - Cubic equation",
        "query": "Solve cubic equation x cubed minus 3x plus 2 equals zero",
        "expected": "alg_001"
    },
    {
        "name": "Test 3: Conceptual match - Taylor series for sine",
        "query": "What is the Taylor expansion of sine function?",
        "expected": "trig_001"
    },
    {
        "name": "Test 4: Low confidence - Unrelated topic",
        "query": "What is the capital of France?",
        "expected": "none (should have low/no confidence)"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{'-' * 80}")
    print(f"{test['name']}")
    print(f"Query: '{test['query']}'")
    print(f"Expected: {test['expected']}")
    print(f"{'-' * 80}")
    
    results = kb.search_similar(test['query'], top_k=3, score_threshold=0.5)
    
    if not results:
        print("❌ No results found")
        continue
    
    print(f"\nTop {len(results)} matches:")
    for j, result in enumerate(results, 1):
        confidence = kb.get_confidence_from_score(result['score'])
        print(f"\n  {j}. Problem ID: {result['problem_id']}")
        print(f"     Similarity: {result['score']:.4f}")
        print(f"     Confidence: {confidence}")
        print(f"     Question: {result['question'][:100]}...")
        print(f"     Topic: {result['topic']} | Difficulty: {result['difficulty']}")

print("\n" + "=" * 80)
print("TESTING COMPLETE")
print("=" * 80)
