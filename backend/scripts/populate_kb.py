"""
Script to populate the Knowledge Base with sample math problems.
Run this to initialize the KB with canonical problems.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vector_db import MathKnowledgeBase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_kb():
    """Populate KB with sample canonical math problems."""
    
    kb = MathKnowledgeBase()
    
    # Sample problems covering different topics
    problems = [
        {
            "problem_id": "calc_001",
            "question": "Evaluate the integral ∫₀¹ x² ln(x) dx",
            "solution_steps": [
                "Use integration by parts with u = ln(x) and dv = x² dx",
                "Then du = (1/x)dx and v = (x³)/3",
                "Apply integration by parts formula: ∫u dv = uv - ∫v du",
                "∫₀¹ x² ln(x) dx = [(x³/3)ln(x)]₀¹ - ∫₀¹ (x³/3)(1/x) dx",
                "= [(x³/3)ln(x)]₀¹ - ∫₀¹ (x²/3) dx",
                "= [(x³/3)ln(x) - x³/9]₀¹",
                "Evaluate at limits: (1/3·0 - 1/9) - lim(x→0⁺)[(x³/3)ln(x) - x³/9]",
                "The limit is 0, so the result is -1/9"
            ],
            "final_answer": "-1/9",
            "difficulty": "JEE_Advanced",
            "tags": ["integration", "integration_by_parts", "logarithm"],
            "topic": "Calculus"
        },
        {
            "problem_id": "calc_002",
            "question": "Find the radius of convergence of the power series ∑(n=1 to ∞) n! xⁿ",
            "solution_steps": [
                "Use the ratio test for convergence",
                "Let aₙ = n! xⁿ",
                "Calculate |aₙ₊₁/aₙ| = |(n+1)! xⁿ⁺¹| / |n! xⁿ|",
                "Simplify: |aₙ₊₁/aₙ| = (n+1)|x|",
                "Take limit as n→∞: lim(n→∞) (n+1)|x| = ∞ for any x ≠ 0",
                "The series converges only when x = 0"
            ],
            "final_answer": "Radius of convergence R = 0",
            "difficulty": "JEE_Advanced",
            "tags": ["series", "convergence", "ratio_test"],
            "topic": "Calculus"
        },
        {
            "problem_id": "calc_003",
            "question": "If f'(x) = 2x/(1+x²) and f(0) = 1, find f(x)",
            "solution_steps": [
                "Integrate f'(x) to find f(x)",
                "∫ 2x/(1+x²) dx",
                "Use substitution: let u = 1+x², then du = 2x dx",
                "∫ 2x/(1+x²) dx = ∫ (1/u) du = ln|u| + C",
                "Substitute back: f(x) = ln(1+x²) + C",
                "Apply initial condition f(0) = 1:",
                "1 = ln(1+0²) + C = ln(1) + C = 0 + C",
                "Therefore C = 1"
            ],
            "final_answer": "f(x) = ln(1+x²) + 1",
            "difficulty": "JEE_Main",
            "tags": ["integration", "differential_equations", "initial_conditions"],
            "topic": "Calculus"
        },
        {
            "problem_id": "alg_001",
            "question": "Solve for x: x³ - 3x + 2 = 0",
            "solution_steps": [
                "Try to factor the cubic polynomial",
                "Test x = 1: 1³ - 3(1) + 2 = 1 - 3 + 2 = 0 ✓",
                "So (x-1) is a factor",
                "Divide x³ - 3x + 2 by (x-1) using polynomial division",
                "x³ - 3x + 2 = (x-1)(x² + x - 2)",
                "Factor the quadratic: x² + x - 2 = (x+2)(x-1)",
                "Complete factorization: (x-1)²(x+2) = 0",
                "Solutions: x = 1 (double root) and x = -2"
            ],
            "final_answer": "x = 1, -2",
            "difficulty": "JEE_Main",
            "tags": ["polynomial", "factoring", "cubic_equations"],
            "topic": "Algebra"
        },
        {
            "problem_id": "trig_001",
            "question": "Find the Maclaurin series for sin(x) up to the x⁵ term",
            "solution_steps": [
                "The Maclaurin series is f(x) = ∑(n=0 to ∞) [f⁽ⁿ⁾(0)/n!] xⁿ",
                "Calculate derivatives of sin(x) at x=0:",
                "f(x) = sin(x), f(0) = 0",
                "f'(x) = cos(x), f'(0) = 1",
                "f''(x) = -sin(x), f''(0) = 0",
                "f'''(x) = -cos(x), f'''(0) = -1",
                "f⁽⁴⁾(x) = sin(x), f⁽⁴⁾(0) = 0",
                "f⁽⁵⁾(x) = cos(x), f⁽⁵⁾(0) = 1",
                "Construct series: sin(x) = 0 + x + 0 - x³/3! + 0 + x⁵/5! + ...",
            ],
            "final_answer": "sin(x) = x - x³/6 + x⁵/120 + O(x⁷)",
            "difficulty": "JEE_Advanced",
            "tags": ["series", "trigonometry", "maclaurin_series"],
            "topic": "Calculus"
        },
        {
            "problem_id": "calc_004",
            "question": "Find the derivative of f(x) = x^x for x > 0",
            "solution_steps": [
                "Take natural logarithm of both sides: ln(f(x)) = ln(x^x)",
                "Simplify: ln(f(x)) = x·ln(x)",
                "Differentiate both sides with respect to x",
                "Left side: d/dx[ln(f(x))] = f'(x)/f(x) (chain rule)",
                "Right side: d/dx[x·ln(x)] = ln(x) + x·(1/x) = ln(x) + 1",
                "Equation: f'(x)/f(x) = ln(x) + 1",
                "Solve for f'(x): f'(x) = f(x)·[ln(x) + 1]",
                "Substitute f(x) = x^x"
            ],
            "final_answer": "f'(x) = x^x·[ln(x) + 1]",
            "difficulty": "JEE_Main",
            "tags": ["derivatives", "logarithmic_differentiation", "exponential"],
            "topic": "Calculus"
        },
        {
            "problem_id": "alg_002",
            "question": "Find all real solutions to √(x+3) + √(x-1) = 4",
            "solution_steps": [
                "Domain: x ≥ 1 (for both square roots to be real)",
                "Isolate one radical: √(x+3) = 4 - √(x-1)",
                "Square both sides: x+3 = 16 - 8√(x-1) + (x-1)",
                "Simplify: x+3 = 15 + x - 8√(x-1)",
                "Isolate radical: 8√(x-1) = 12",
                "Divide by 8: √(x-1) = 3/2",
                "Square again: x-1 = 9/4",
                "Solve: x = 1 + 9/4 = 13/4",
                "Verify: √(13/4+3) + √(13/4-1) = √(25/4) + √(9/4) = 5/2 + 3/2 = 4 ✓"
            ],
            "final_answer": "x = 13/4 = 3.25",
            "difficulty": "JEE_Main",
            "tags": ["radicals", "equations", "algebraic_manipulation"],
            "topic": "Algebra"
        },
        {
            "problem_id": "calc_005",
            "question": "Evaluate lim(x→0) [sin(x)/x]",
            "solution_steps": [
                "This is an indeterminate form 0/0",
                "Method 1 - L'Hôpital's Rule:",
                "Differentiate numerator and denominator",
                "lim(x→0) [cos(x)/1] = cos(0) = 1",
                "Method 2 - Geometric approach:",
                "Consider unit circle: sin(x) < x < tan(x) for small x > 0",
                "Divide by sin(x): 1 < x/sin(x) < 1/cos(x)",
                "Take reciprocals: 1 > sin(x)/x > cos(x)",
                "As x→0, cos(x)→1, so by squeeze theorem sin(x)/x→1"
            ],
            "final_answer": "1",
            "difficulty": "JEE_Main",
            "tags": ["limits", "trigonometry", "lhopital"],
            "topic": "Calculus"
        },
        {
            "problem_id": "geom_001",
            "question": "Find the equation of a circle passing through (0,0), (4,0), and (0,3)",
            "solution_steps": [
                "General equation of circle: (x-h)² + (y-k)² = r²",
                "Or expanded: x² + y² + Dx + Ey + F = 0",
                "Substitute (0,0): 0 + 0 + 0 + 0 + F = 0, so F = 0",
                "Substitute (4,0): 16 + 0 + 4D + 0 + 0 = 0, so D = -4",
                "Substitute (0,3): 0 + 9 + 0 + 3E + 0 = 0, so E = -3",
                "Equation: x² + y² - 4x - 3y = 0",
                "Complete the square: (x-2)² - 4 + (y-3/2)² - 9/4 = 0",
                "Standard form: (x-2)² + (y-3/2)² = 25/4",
                "Center: (2, 3/2), Radius: 5/2"
            ],
            "final_answer": "x² + y² - 4x - 3y = 0 or (x-2)² + (y-3/2)² = 25/4",
            "difficulty": "JEE_Main",
            "tags": ["geometry", "circle", "coordinate_geometry"],
            "topic": "Geometry"
        },
        {
            "problem_id": "prob_001",
            "question": "A box contains 5 red balls and 3 blue balls. If 3 balls are drawn without replacement, what is the probability that exactly 2 are red?",
            "solution_steps": [
                "Total balls = 5 red + 3 blue = 8 balls",
                "Total ways to choose 3 balls from 8: C(8,3)",
                "C(8,3) = 8!/(3!·5!) = 56",
                "Ways to choose exactly 2 red and 1 blue:",
                "Choose 2 red from 5: C(5,2) = 10",
                "Choose 1 blue from 3: C(3,1) = 3",
                "Favorable outcomes: C(5,2) × C(3,1) = 10 × 3 = 30",
                "Probability = Favorable/Total = 30/56 = 15/28"
            ],
            "final_answer": "15/28 ≈ 0.536",
            "difficulty": "JEE_Main",
            "tags": ["probability", "combinations", "without_replacement"],
            "topic": "Probability"
        }
    ]
    
    # Add all problems to KB
    for problem in problems:
        try:
            kb.add_problem(**problem)
            logger.info(f"✓ Added: {problem['problem_id']} - {problem['question'][:50]}...")
        except Exception as e:
            logger.error(f"✗ Failed to add {problem['problem_id']}: {e}")
    
    # Summary
    total_count = kb.count_problems()
    logger.info(f"\n{'='*60}")
    logger.info(f"KB Population Complete!")
    logger.info(f"Total problems in KB: {total_count}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    populate_kb()
