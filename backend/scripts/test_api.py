"""
Comprehensive API Testing Script
Populates KB first, then tests various query scenarios
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.vector_db import MathKnowledgeBase
import requests
import json
import time

print("=" * 90)
print("STEP 1: POPULATING KNOWLEDGE BASE")
print("=" * 90)

# Initialize and populate KB
kb = MathKnowledgeBase()

# Full set of 10 problems from populate_kb.py
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

for problem in problems:
    kb.add_problem(**problem)
    print(f"✓ {problem['problem_id']}")

print(f"\n✓ Total problems loaded: {kb.count_problems()}\n")

print("=" * 90)
print("STEP 2: TESTING API ENDPOINTS")
print("=" * 90)
print("Waiting for API to be ready...")
time.sleep(2)

# API Tests
test_cases = [
    {
        "name": "🎯 Test 1: HIGH CONFIDENCE - Integration (exact match)",
        "query": {
            "question": "How to evaluate integral of x squared times ln(x) from 0 to 1?",
            "difficulty": "JEE_Advanced"
        },
        "expected": "calc_001 with high/medium confidence"
    },
    {
        "name": "🎯 Test 2: MEDIUM CONFIDENCE - Cubic equation",
        "query": {
            "question": "Solve the cubic x³ - 3x + 2 = 0",
            "difficulty": "JEE_Main"
        },
        "expected": "alg_001 with medium confidence"
    },
    {
        "name": "🎯 Test 3: DERIVATIVE - x to the power x",
        "query": {
            "question": "What is the derivative of x to the power of x?",
            "difficulty": "JEE_Advanced"
        },
        "expected": "calc_004"
    },
    {
        "name": "🎯 Test 4: PROBABILITY - Ball selection",
        "query": {
            "question": "Red balls and blue balls probability with 3 selections",
            "difficulty": "JEE_Main"
        },
        "expected": "prob_001"
    },
    {
        "name": "❌ Test 5: LOW/NONE - Unrelated (should use external API)",
        "query": {
            "question": "Explain matrix multiplication and its properties",
            "difficulty": "JEE_Main"
        },
        "expected": "External API fallback (no KB match)"
    }
]

api_url = "http://127.0.0.1:8000/query"

for i, test in enumerate(test_cases, 1):
    print(f"\n{'-' * 90}")
    print(f"{test['name']}")
    print(f"Query: '{test['query']['question']}'")
    print(f"Expected: {test['expected']}")
    print(f"{'-' * 90}")
    
    try:
        response = requests.post(api_url, json=test['query'], timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            confidence = result.get('confidence', 'N/A')
            score = result.get('confidence_score', 0)
            source = result.get('source', 'N/A')
            
            print(f"✅ Status: 200 OK")
            print(f"📊 Confidence: {confidence.upper()} (score: {score:.4f})")
            print(f"🔍 Source: {source}")
            
            # KB Results
            kb_matches = result.get('kb_results', [])
            if kb_matches:
                print(f"\n📚 KB Matches ({len(kb_matches)}):")
                for j, match in enumerate(kb_matches[:2], 1):
                    pid = match.get('problem_id', 'N/A')
                    mscore = match.get('score', 0)
                    print(f"   {j}. {pid} - Score: {mscore:.4f}")
            else:
                print(f"\n📚 KB Matches: None")
            
            # Answer preview
            answer = result.get('answer', '')
            if answer and len(answer) > 150:
                print(f"\n💡 Answer: {answer[:150]}...")
            elif answer:
                print(f"\n💡 Answer: {answer}")
            
            # Steps
            steps = result.get('reasoning_steps', [])
            if steps:
                print(f"📝 Steps provided: {len(steps)}")
                
        else:
            print(f"❌ HTTP {response.status_code}")
            print(f"Error: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running on http://127.0.0.1:8000")
        print("   Please start server: uvicorn app.main:app --reload")
        break
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n{'=' * 90}")
print("API TESTING COMPLETE!")
print("=" * 90)
