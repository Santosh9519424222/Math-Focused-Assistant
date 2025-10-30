"""
Expand Knowledge Base to 50+ Problems
Adds 45+ JEE-level math problems across all topics
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vector_db import MathKnowledgeBase

def expand_knowledge_base():
    """Add 45+ new problems to reach 50+ total"""
    
    kb = MathKnowledgeBase()
    
    print("=" * 70)
    print("  EXPANDING KNOWLEDGE BASE TO 50+ PROBLEMS")
    print("=" * 70)
    
    # Get current count
    try:
        current_count = kb.client.count(collection_name=kb.collection_name).count
        print(f"\nCurrent KB size: {current_count} problems")
    except:
        current_count = 0
        print(f"\nStarting fresh knowledge base")
    
    print("\nAdding problems across all JEE topics...")
    print("-" * 70)
    
    problems_added = 0
    
    # ==================== CALCULUS PROBLEMS (15) ====================
    print("\n📐 Adding CALCULUS problems...")
    
    calculus_problems = [
        {
            "problem_id": "calc_002",
            "question": "Find the derivative of f(x) = x^x with respect to x",
            "solution_steps": [
                "Let y = x^x",
                "Take natural log of both sides: ln(y) = ln(x^x) = x·ln(x)",
                "Differentiate both sides with respect to x using implicit differentiation",
                "Left side: (1/y)·(dy/dx)",
                "Right side: d/dx[x·ln(x)] = ln(x) + x·(1/x) = ln(x) + 1",
                "Therefore: (1/y)·(dy/dx) = ln(x) + 1",
                "Multiply both sides by y: dy/dx = y(ln(x) + 1)",
                "Substitute y = x^x back: dy/dx = x^x(ln(x) + 1)"
            ],
            "final_answer": "d/dx[x^x] = x^x(ln(x) + 1)",
            "difficulty": "JEE_Advanced",
            "tags": ["calculus", "differentiation", "logarithmic differentiation", "exponential functions"],
            "topic": "Calculus - Differentiation"
        },
        {
            "problem_id": "calc_003",
            "question": "Evaluate the limit: lim(x→0) [sin(x) - x] / x³",
            "solution_steps": [
                "Direct substitution gives 0/0 (indeterminate form)",
                "Apply L'Hôpital's rule (differentiate numerator and denominator)",
                "First application: lim(x→0) [cos(x) - 1] / 3x²",
                "Still 0/0, apply L'Hôpital's rule again",
                "Second application: lim(x→0) [-sin(x)] / 6x",
                "Still 0/0, apply L'Hôpital's rule once more",
                "Third application: lim(x→0) [-cos(x)] / 6",
                "Now we can substitute x = 0: -cos(0) / 6 = -1/6"
            ],
            "final_answer": "-1/6",
            "difficulty": "JEE_Advanced",
            "tags": ["calculus", "limits", "L'Hôpital's rule", "indeterminate forms"],
            "topic": "Calculus - Limits"
        },
        {
            "problem_id": "calc_004",
            "question": "Find the area under the curve y = e^(-x²) from x = 0 to x = ∞",
            "solution_steps": [
                "This is the Gaussian integral: ∫₀^∞ e^(-x²) dx",
                "Consider the double integral: I² = (∫₀^∞ e^(-x²) dx)(∫₀^∞ e^(-y²) dy)",
                "Combine: I² = ∫∫ e^(-(x²+y²)) dx dy over first quadrant",
                "Convert to polar coordinates: x² + y² = r², dx dy = r dr dθ",
                "I² = ∫₀^(π/2) ∫₀^∞ e^(-r²) r dr dθ",
                "Inner integral: ∫₀^∞ e^(-r²) r dr = [-1/2 e^(-r²)]₀^∞ = 1/2",
                "Outer integral: ∫₀^(π/2) (1/2) dθ = π/4",
                "Therefore I² = π/4, so I = √(π/4) = √π/2"
            ],
            "final_answer": "√π/2 ≈ 0.886",
            "difficulty": "JEE_Advanced",
            "tags": ["calculus", "definite integrals", "gaussian integral", "polar coordinates"],
            "topic": "Calculus - Integration"
        },
        {
            "problem_id": "calc_005",
            "question": "Find the Maclaurin series expansion for f(x) = e^x up to the x⁵ term",
            "solution_steps": [
                "Maclaurin series: f(x) = f(0) + f'(0)x + f''(0)x²/2! + f'''(0)x³/3! + ...",
                "For f(x) = e^x, all derivatives are e^x",
                "f(0) = e^0 = 1",
                "f'(0) = e^0 = 1",
                "f''(0) = e^0 = 1",
                "f'''(0) = e^0 = 1",
                "f⁽⁴⁾(0) = e^0 = 1",
                "f⁽⁵⁾(0) = e^0 = 1",
                "Series: e^x = 1 + x + x²/2! + x³/3! + x⁴/4! + x⁵/5! + ...",
                "Up to x⁵: e^x ≈ 1 + x + x²/2 + x³/6 + x⁴/24 + x⁵/120"
            ],
            "final_answer": "e^x ≈ 1 + x + x²/2 + x³/6 + x⁴/24 + x⁵/120",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "series", "taylor series", "maclaurin series", "exponential"],
            "topic": "Calculus - Series"
        },
        {
            "problem_id": "calc_006",
            "question": "Find the local maximum and minimum of f(x) = x³ - 6x² + 9x + 1",
            "solution_steps": [
                "Find critical points by setting f'(x) = 0",
                "f'(x) = 3x² - 12x + 9",
                "Set f'(x) = 0: 3x² - 12x + 9 = 0",
                "Divide by 3: x² - 4x + 3 = 0",
                "Factor: (x - 1)(x - 3) = 0",
                "Critical points: x = 1 and x = 3",
                "Use second derivative test: f''(x) = 6x - 12",
                "At x = 1: f''(1) = 6(1) - 12 = -6 < 0, so local maximum",
                "At x = 3: f''(3) = 6(3) - 12 = 6 > 0, so local minimum",
                "f(1) = 1 - 6 + 9 + 1 = 5 (local max)",
                "f(3) = 27 - 54 + 27 + 1 = 1 (local min)"
            ],
            "final_answer": "Local maximum at (1, 5), Local minimum at (3, 1)",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "optimization", "critical points", "maxima minima"],
            "topic": "Calculus - Optimization"
        },
        {
            "problem_id": "calc_007",
            "question": "Solve the differential equation dy/dx = y/x with initial condition y(1) = 2",
            "solution_steps": [
                "This is a separable differential equation",
                "Separate variables: dy/y = dx/x",
                "Integrate both sides: ∫(dy/y) = ∫(dx/x)",
                "ln|y| = ln|x| + C",
                "Exponentiate: |y| = e^(ln|x| + C) = e^C · |x|",
                "Let k = ±e^C: y = kx",
                "Apply initial condition y(1) = 2: 2 = k(1), so k = 2",
                "Therefore: y = 2x"
            ],
            "final_answer": "y = 2x",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "differential equations", "separable equations"],
            "topic": "Calculus - Differential Equations"
        },
        {
            "problem_id": "calc_008",
            "question": "Find ∫ x·sin(x) dx using integration by parts",
            "solution_steps": [
                "Use integration by parts: ∫u dv = uv - ∫v du",
                "Let u = x, so du = dx",
                "Let dv = sin(x) dx, so v = -cos(x)",
                "Apply formula: ∫x·sin(x) dx = x(-cos(x)) - ∫(-cos(x)) dx",
                "Simplify: = -x·cos(x) + ∫cos(x) dx",
                "= -x·cos(x) + sin(x) + C"
            ],
            "final_answer": "∫x·sin(x) dx = -x·cos(x) + sin(x) + C",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "integration", "integration by parts"],
            "topic": "Calculus - Integration"
        },
        {
            "problem_id": "calc_009",
            "question": "Find the volume of solid formed by rotating y = √x from x=0 to x=4 about the x-axis",
            "solution_steps": [
                "Use disk method: V = π∫[a to b] [f(x)]² dx",
                "Here f(x) = √x, a = 0, b = 4",
                "V = π∫₀⁴ (√x)² dx",
                "V = π∫₀⁴ x dx",
                "V = π[x²/2]₀⁴",
                "V = π[(4²/2) - (0²/2)]",
                "V = π[16/2 - 0]",
                "V = 8π cubic units"
            ],
            "final_answer": "8π cubic units ≈ 25.13 cubic units",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "volumes", "solid of revolution", "disk method"],
            "topic": "Calculus - Applications"
        },
        {
            "problem_id": "calc_010",
            "question": "Find the arc length of y = x^(3/2) from x = 0 to x = 4",
            "solution_steps": [
                "Arc length formula: L = ∫[a to b] √(1 + (dy/dx)²) dx",
                "Find dy/dx: dy/dx = (3/2)x^(1/2) = (3/2)√x",
                "(dy/dx)² = (9/4)x",
                "L = ∫₀⁴ √(1 + (9/4)x) dx",
                "Let u = 1 + (9/4)x, then du = (9/4)dx, dx = (4/9)du",
                "When x = 0: u = 1; When x = 4: u = 10",
                "L = (4/9)∫₁¹⁰ √u du",
                "L = (4/9) · (2/3)u^(3/2)|₁¹⁰",
                "L = (8/27)[10^(3/2) - 1]",
                "L = (8/27)[10√10 - 1] ≈ 9.07 units"
            ],
            "final_answer": "(8/27)(10√10 - 1) ≈ 9.07 units",
            "difficulty": "JEE_Advanced",
            "tags": ["calculus", "arc length", "integration", "applications"],
            "topic": "Calculus - Applications"
        },
        {
            "problem_id": "calc_011",
            "question": "Evaluate ∫ 1/(x² + 4) dx",
            "solution_steps": [
                "Recognize this as an inverse tangent integral form",
                "Standard form: ∫ 1/(x² + a²) dx = (1/a)arctan(x/a) + C",
                "Here a² = 4, so a = 2",
                "Apply formula: ∫ 1/(x² + 4) dx = (1/2)arctan(x/2) + C"
            ],
            "final_answer": "(1/2)arctan(x/2) + C",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "integration", "inverse trigonometric", "standard forms"],
            "topic": "Calculus - Integration"
        },
        {
            "problem_id": "calc_012",
            "question": "Find dy/dx if y = ln(sin(x))",
            "solution_steps": [
                "Use chain rule: dy/dx = d/dx[ln(sin(x))]",
                "= (1/sin(x)) · d/dx[sin(x)]",
                "= (1/sin(x)) · cos(x)",
                "= cos(x)/sin(x)",
                "= cot(x)"
            ],
            "final_answer": "dy/dx = cot(x)",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "differentiation", "chain rule", "logarithmic"],
            "topic": "Calculus - Differentiation"
        },
        {
            "problem_id": "calc_013",
            "question": "Find the inflection points of f(x) = x⁴ - 4x³",
            "solution_steps": [
                "Inflection points occur where f''(x) = 0 and f'' changes sign",
                "Find first derivative: f'(x) = 4x³ - 12x²",
                "Find second derivative: f''(x) = 12x² - 24x",
                "Set f''(x) = 0: 12x² - 24x = 0",
                "Factor: 12x(x - 2) = 0",
                "Solutions: x = 0 or x = 2",
                "Check sign changes:",
                "For x < 0: f''(-1) = 12 + 24 = 36 > 0 (concave up)",
                "For 0 < x < 2: f''(1) = 12 - 24 = -12 < 0 (concave down)",
                "For x > 2: f''(3) = 108 - 72 = 36 > 0 (concave up)",
                "Both x = 0 and x = 2 are inflection points",
                "f(0) = 0, f(2) = 16 - 32 = -16"
            ],
            "final_answer": "Inflection points at (0, 0) and (2, -16)",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "concavity", "inflection points", "second derivative"],
            "topic": "Calculus - Applications"
        },
        {
            "problem_id": "calc_014",
            "question": "Find lim(x→∞) (x² + 3x)/(2x² + x - 1)",
            "solution_steps": [
                "Divide numerator and denominator by highest power: x²",
                "lim(x→∞) [(x²/x² + 3x/x²)/(2x²/x² + x/x² - 1/x²)]",
                "= lim(x→∞) [(1 + 3/x)/(2 + 1/x - 1/x²)]",
                "As x → ∞: 3/x → 0, 1/x → 0, 1/x² → 0",
                "= (1 + 0)/(2 + 0 - 0)",
                "= 1/2"
            ],
            "final_answer": "1/2",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "limits", "limits at infinity", "rational functions"],
            "topic": "Calculus - Limits"
        },
        {
            "problem_id": "calc_015",
            "question": "Evaluate ∫₀^(π/2) sin²(x) dx",
            "solution_steps": [
                "Use power reduction formula: sin²(x) = (1 - cos(2x))/2",
                "∫₀^(π/2) sin²(x) dx = ∫₀^(π/2) (1 - cos(2x))/2 dx",
                "= (1/2)∫₀^(π/2) [1 - cos(2x)] dx",
                "= (1/2)[x - sin(2x)/2]₀^(π/2)",
                "= (1/2)[(π/2 - sin(π)/2) - (0 - sin(0)/2)]",
                "= (1/2)[(π/2 - 0) - (0 - 0)]",
                "= (1/2)(π/2)",
                "= π/4"
            ],
            "final_answer": "π/4",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "definite integrals", "trigonometric integrals", "power reduction"],
            "topic": "Calculus - Integration"
        },
        {
            "problem_id": "calc_016",
            "question": "Find the equation of the tangent line to y = x³ at the point (2, 8)",
            "solution_steps": [
                "Find the slope at x = 2 using derivative",
                "dy/dx = 3x²",
                "At x = 2: m = 3(2)² = 12",
                "Use point-slope form: y - y₁ = m(x - x₁)",
                "y - 8 = 12(x - 2)",
                "y - 8 = 12x - 24",
                "y = 12x - 16"
            ],
            "final_answer": "y = 12x - 16",
            "difficulty": "JEE_Main",
            "tags": ["calculus", "tangent lines", "differentiation", "applications"],
            "topic": "Calculus - Applications"
        }
    ]
    
    for problem in calculus_problems:
        kb.add_problem(**problem)
        problems_added += 1
        print(f"  ✓ Added {problem['problem_id']}: {problem['question'][:50]}...")
    
    # ==================== ALGEBRA PROBLEMS (10) ====================
    print("\n🔢 Adding ALGEBRA problems...")
    
    algebra_problems = [
        {
            "problem_id": "alg_002",
            "question": "Solve the system of equations: 2x + 3y = 7 and 4x - y = 5",
            "solution_steps": [
                "From second equation: y = 4x - 5",
                "Substitute into first equation: 2x + 3(4x - 5) = 7",
                "2x + 12x - 15 = 7",
                "14x = 22",
                "x = 22/14 = 11/7",
                "Substitute back: y = 4(11/7) - 5 = 44/7 - 35/7 = 9/7"
            ],
            "final_answer": "x = 11/7, y = 9/7",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "linear equations", "systems", "substitution"],
            "topic": "Algebra - Linear Equations"
        },
        {
            "problem_id": "alg_003",
            "question": "Find all roots of the polynomial x⁴ - 5x² + 4 = 0",
            "solution_steps": [
                "This is a biquadratic equation",
                "Let u = x², then u² - 5u + 4 = 0",
                "Factor: (u - 1)(u - 4) = 0",
                "Solutions: u = 1 or u = 4",
                "For u = 1: x² = 1, so x = ±1",
                "For u = 4: x² = 4, so x = ±2",
                "Four roots: x = -2, -1, 1, 2"
            ],
            "final_answer": "x = -2, -1, 1, 2",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "polynomials", "biquadratic", "factoring"],
            "topic": "Algebra - Polynomials"
        },
        {
            "problem_id": "alg_004",
            "question": "Solve the inequality |2x - 3| < 5",
            "solution_steps": [
                "Absolute value inequality: |A| < B means -B < A < B",
                "Apply to |2x - 3| < 5: -5 < 2x - 3 < 5",
                "Add 3 to all parts: -5 + 3 < 2x < 5 + 3",
                "-2 < 2x < 8",
                "Divide by 2: -1 < x < 4",
                "Solution in interval notation: (-1, 4)"
            ],
            "final_answer": "-1 < x < 4 or x ∈ (-1, 4)",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "inequalities", "absolute value"],
            "topic": "Algebra - Inequalities"
        },
        {
            "problem_id": "alg_005",
            "question": "Find the sum of the first 20 terms of the arithmetic sequence: 3, 7, 11, 15, ...",
            "solution_steps": [
                "Identify: First term a = 3, common difference d = 4",
                "Formula for nth term: aₙ = a + (n-1)d",
                "20th term: a₂₀ = 3 + (20-1)(4) = 3 + 76 = 79",
                "Sum formula: Sₙ = n/2 (first term + last term)",
                "S₂₀ = 20/2 (3 + 79)",
                "S₂₀ = 10 × 82",
                "S₂₀ = 820"
            ],
            "final_answer": "820",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "sequences", "arithmetic progression", "series"],
            "topic": "Algebra - Sequences"
        },
        {
            "problem_id": "alg_006",
            "question": "Simplify log₂(8) + log₃(27) - log₅(125)",
            "solution_steps": [
                "Evaluate each logarithm separately",
                "log₂(8): 2³ = 8, so log₂(8) = 3",
                "log₃(27): 3³ = 27, so log₃(27) = 3",
                "log₅(125): 5³ = 125, so log₅(125) = 3",
                "Combine: 3 + 3 - 3 = 3"
            ],
            "final_answer": "3",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "logarithms", "properties"],
            "topic": "Algebra - Logarithms"
        },
        {
            "problem_id": "alg_007",
            "question": "Find the coefficient of x⁵ in the expansion of (2x + 3)⁷",
            "solution_steps": [
                "Use binomial theorem: (a+b)ⁿ = Σ C(n,k) aⁿ⁻ᵏ bᵏ",
                "Here a = 2x, b = 3, n = 7",
                "For x⁵ term, we need (2x)⁵ with k = 2 (since 7-k=5)",
                "Term: C(7,2) · (2x)⁵ · 3²",
                "C(7,2) = 7!/(2!5!) = 21",
                "(2x)⁵ = 32x⁵",
                "3² = 9",
                "Coefficient: 21 × 32 × 9 = 6048"
            ],
            "final_answer": "6048",
            "difficulty": "JEE_Advanced",
            "tags": ["algebra", "binomial theorem", "expansions"],
            "topic": "Algebra - Binomial Theorem"
        },
        {
            "problem_id": "alg_008",
            "question": "Solve for x: 2^(x+1) = 32",
            "solution_steps": [
                "Rewrite 32 as a power of 2: 32 = 2⁵",
                "Equation becomes: 2^(x+1) = 2⁵",
                "Since bases are equal, equate exponents: x + 1 = 5",
                "Solve for x: x = 5 - 1 = 4"
            ],
            "final_answer": "x = 4",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "exponential equations", "powers"],
            "topic": "Algebra - Exponentials"
        },
        {
            "problem_id": "alg_009",
            "question": "Find the sum to infinity of the geometric series: 1 + 1/3 + 1/9 + 1/27 + ...",
            "solution_steps": [
                "Identify: First term a = 1, common ratio r = 1/3",
                "Check convergence: |r| = 1/3 < 1, so series converges",
                "Formula for infinite geometric series: S = a/(1-r)",
                "S = 1/(1 - 1/3)",
                "S = 1/(2/3)",
                "S = 3/2"
            ],
            "final_answer": "3/2 or 1.5",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "geometric series", "infinite series", "convergence"],
            "topic": "Algebra - Series"
        },
        {
            "problem_id": "alg_010",
            "question": "Factor completely: x³ + 8",
            "solution_steps": [
                "Recognize as sum of cubes: a³ + b³",
                "Here a = x, b = 2 (since 2³ = 8)",
                "Formula: a³ + b³ = (a + b)(a² - ab + b²)",
                "Apply: x³ + 8 = (x + 2)(x² - 2x + 4)",
                "Check if second factor can be factored (discriminant test)",
                "Discriminant: (-2)² - 4(1)(4) = 4 - 16 = -12 < 0",
                "Second factor has no real factors"
            ],
            "final_answer": "(x + 2)(x² - 2x + 4)",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "factoring", "sum of cubes", "polynomials"],
            "topic": "Algebra - Factoring"
        },
        {
            "problem_id": "alg_011",
            "question": "Solve the quadratic inequality x² - 5x + 6 < 0",
            "solution_steps": [
                "First, find roots of x² - 5x + 6 = 0",
                "Factor: (x - 2)(x - 3) = 0",
                "Roots: x = 2 and x = 3",
                "Test intervals: (-∞, 2), (2, 3), (3, ∞)",
                "For x < 2 (test x=0): 0 - 0 + 6 = 6 > 0 ✗",
                "For 2 < x < 3 (test x=2.5): 6.25 - 12.5 + 6 = -0.25 < 0 ✓",
                "For x > 3 (test x=4): 16 - 20 + 6 = 2 > 0 ✗",
                "Solution: 2 < x < 3"
            ],
            "final_answer": "2 < x < 3 or x ∈ (2, 3)",
            "difficulty": "JEE_Main",
            "tags": ["algebra", "quadratic inequalities", "interval testing"],
            "topic": "Algebra - Inequalities"
        }
    ]
    
    for problem in algebra_problems:
        kb.add_problem(**problem)
        problems_added += 1
        print(f"  ✓ Added {problem['problem_id']}: {problem['question'][:50]}...")
    
    # ==================== TRIGONOMETRY PROBLEMS (5) ====================
    print("\n📐 Adding TRIGONOMETRY problems...")
    
    trig_problems = [
        {
            "problem_id": "trig_002",
            "question": "Prove the identity: sin(2x) = 2sin(x)cos(x)",
            "solution_steps": [
                "Start with addition formula: sin(A + B) = sin(A)cos(B) + cos(A)sin(B)",
                "Let A = x and B = x",
                "sin(x + x) = sin(x)cos(x) + cos(x)sin(x)",
                "sin(2x) = sin(x)cos(x) + sin(x)cos(x)",
                "sin(2x) = 2sin(x)cos(x)",
                "Identity proved ✓"
            ],
            "final_answer": "sin(2x) = 2sin(x)cos(x) [Proved]",
            "difficulty": "JEE_Main",
            "tags": ["trigonometry", "identities", "double angle", "proofs"],
            "topic": "Trigonometry - Identities"
        },
        {
            "problem_id": "trig_003",
            "question": "Solve for x in [0, 2π]: sin(x) = 1/2",
            "solution_steps": [
                "Recall: sin(π/6) = 1/2",
                "General solution: x = nπ + (-1)ⁿ(π/6), n ∈ ℤ",
                "For n = 0: x = 0 + π/6 = π/6 ✓ (in [0, 2π])",
                "For n = 1: x = π - π/6 = 5π/6 ✓ (in [0, 2π])",
                "For n = 2: x = 2π + π/6 = 13π/6 ✗ (outside [0, 2π])",
                "Solutions in [0, 2π]: x = π/6 and x = 5π/6"
            ],
            "final_answer": "x = π/6 and x = 5π/6",
            "difficulty": "JEE_Main",
            "tags": ["trigonometry", "equations", "inverse trig"],
            "topic": "Trigonometry - Equations"
        },
        {
            "problem_id": "trig_004",
            "question": "Find the value of cos(15°)",
            "solution_steps": [
                "Use angle subtraction: 15° = 45° - 30°",
                "Formula: cos(A - B) = cos(A)cos(B) + sin(A)sin(B)",
                "cos(15°) = cos(45° - 30°)",
                "= cos(45°)cos(30°) + sin(45°)sin(30°)",
                "= (√2/2)(√3/2) + (√2/2)(1/2)",
                "= (√6/4) + (√2/4)",
                "= (√6 + √2)/4"
            ],
            "final_answer": "(√6 + √2)/4 ≈ 0.9659",
            "difficulty": "JEE_Main",
            "tags": ["trigonometry", "compound angles", "special angles"],
            "topic": "Trigonometry - Values"
        },
        {
            "problem_id": "trig_005",
            "question": "Simplify: (1 + tan²θ)",
            "solution_steps": [
                "Recall identity: 1 + tan²θ = sec²θ",
                "Proof: Start with sin²θ + cos²θ = 1",
                "Divide both sides by cos²θ:",
                "sin²θ/cos²θ + cos²θ/cos²θ = 1/cos²θ",
                "tan²θ + 1 = sec²θ",
                "Therefore: 1 + tan²θ = sec²θ"
            ],
            "final_answer": "sec²θ",
            "difficulty": "JEE_Main",
            "tags": ["trigonometry", "identities", "pythagorean"],
            "topic": "Trigonometry - Identities"
        },
        {
            "problem_id": "trig_006",
            "question": "Find the period of f(x) = sin(3x) + cos(2x)",
            "solution_steps": [
                "Period of sin(3x): T₁ = 2π/3",
                "Period of cos(2x): T₂ = 2π/2 = π",
                "Period of sum = LCM(T₁, T₂)",
                "Express as fractions: 2π/3 and π = 3π/3",
                "LCM of numerators: LCM(2π, 3π) = 6π",
                "GCD of denominators: GCD(3, 3) = 3",
                "Period = 6π/3 = 2π"
            ],
            "final_answer": "2π",
            "difficulty": "JEE_Advanced",
            "tags": ["trigonometry", "periodicity", "functions"],
            "topic": "Trigonometry - Functions"
        }
    ]
    
    for problem in trig_problems:
        kb.add_problem(**problem)
        problems_added += 1
        print(f"  ✓ Added {problem['problem_id']}: {problem['question'][:50]}...")
    
    # ==================== GEOMETRY PROBLEMS (5) ====================
    print("\n📏 Adding GEOMETRY problems...")
    
    geometry_problems = [
        {
            "problem_id": "geom_001",
            "question": "Find the area of a triangle with sides 5, 12, and 13",
            "solution_steps": [
                "Check if right triangle: 5² + 12² = 25 + 144 = 169 = 13²",
                "Yes, it's a right triangle with legs 5 and 12",
                "Area = (1/2) × base × height",
                "Area = (1/2) × 5 × 12",
                "Area = 30 square units"
            ],
            "final_answer": "30 square units",
            "difficulty": "JEE_Main",
            "tags": ["geometry", "triangles", "area", "pythagorean"],
            "topic": "Geometry - Triangles"
        },
        {
            "problem_id": "geom_002",
            "question": "Find the equation of a circle with center (3, -2) and radius 5",
            "solution_steps": [
                "Standard form: (x - h)² + (y - k)² = r²",
                "Here center (h, k) = (3, -2), radius r = 5",
                "Substitute: (x - 3)² + (y - (-2))² = 5²",
                "(x - 3)² + (y + 2)² = 25"
            ],
            "final_answer": "(x - 3)² + (y + 2)² = 25",
            "difficulty": "JEE_Main",
            "tags": ["geometry", "circles", "coordinate geometry", "equations"],
            "topic": "Geometry - Circles"
        },
        {
            "problem_id": "geom_003",
            "question": "Find the distance between points A(1, 2) and B(4, 6)",
            "solution_steps": [
                "Use distance formula: d = √[(x₂-x₁)² + (y₂-y₁)²]",
                "d = √[(4-1)² + (6-2)²]",
                "d = √[3² + 4²]",
                "d = √[9 + 16]",
                "d = √25",
                "d = 5 units"
            ],
            "final_answer": "5 units",
            "difficulty": "JEE_Main",
            "tags": ["geometry", "coordinate geometry", "distance formula"],
            "topic": "Geometry - Coordinate Geometry"
        },
        {
            "problem_id": "geom_004",
            "question": "Find the volume of a sphere with radius 3 cm",
            "solution_steps": [
                "Volume formula: V = (4/3)πr³",
                "Substitute r = 3:",
                "V = (4/3)π(3)³",
                "V = (4/3)π(27)",
                "V = (4 × 27π)/3",
                "V = 108π/3",
                "V = 36π cm³",
                "V ≈ 113.10 cm³"
            ],
            "final_answer": "36π cm³ ≈ 113.10 cm³",
            "difficulty": "JEE_Main",
            "tags": ["geometry", "3d geometry", "volume", "sphere"],
            "topic": "Geometry - 3D Shapes"
        },
        {
            "problem_id": "geom_005",
            "question": "Find the slope of the line passing through (2, 3) and (5, 9)",
            "solution_steps": [
                "Slope formula: m = (y₂ - y₁)/(x₂ - x₁)",
                "m = (9 - 3)/(5 - 2)",
                "m = 6/3",
                "m = 2"
            ],
            "final_answer": "m = 2",
            "difficulty": "JEE_Main",
            "tags": ["geometry", "coordinate geometry", "slope", "lines"],
            "topic": "Geometry - Lines"
        }
    ]
    
    for problem in geometry_problems:
        kb.add_problem(**problem)
        problems_added += 1
        print(f"  ✓ Added {problem['problem_id']}: {problem['question'][:50]}...")
    
    # ==================== PROBABILITY PROBLEMS (5) ====================
    print("\n🎲 Adding PROBABILITY problems...")
    
    probability_problems = [
        {
            "problem_id": "prob_002",
            "question": "What is the probability of getting at least one head in three coin tosses?",
            "solution_steps": [
                "Use complement: P(at least one H) = 1 - P(no heads)",
                "P(no heads) = P(all tails)",
                "Each toss: P(T) = 1/2",
                "Three independent tosses: P(TTT) = (1/2)³ = 1/8",
                "P(at least one H) = 1 - 1/8 = 7/8"
            ],
            "final_answer": "7/8 or 0.875",
            "difficulty": "JEE_Main",
            "tags": ["probability", "coins", "complement", "independent events"],
            "topic": "Probability - Basic"
        },
        {
            "problem_id": "prob_003",
            "question": "A box contains 3 red and 2 blue balls. Find P(both red) if drawn without replacement",
            "solution_steps": [
                "First draw: P(red) = 3/5",
                "Second draw (given first was red): P(red|first red) = 2/4 = 1/2",
                "Total balls after first draw: 4 remaining, 2 red",
                "P(both red) = P(first red) × P(second red|first red)",
                "P(both red) = (3/5) × (1/2)",
                "P(both red) = 3/10 = 0.3"
            ],
            "final_answer": "3/10 or 0.3",
            "difficulty": "JEE_Main",
            "tags": ["probability", "conditional", "without replacement"],
            "topic": "Probability - Conditional"
        },
        {
            "problem_id": "prob_004",
            "question": "Find the expected value of a fair six-sided die",
            "solution_steps": [
                "Expected value E(X) = Σ x·P(x)",
                "For fair die: P(x) = 1/6 for x = 1, 2, 3, 4, 5, 6",
                "E(X) = 1·(1/6) + 2·(1/6) + 3·(1/6) + 4·(1/6) + 5·(1/6) + 6·(1/6)",
                "E(X) = (1/6)(1 + 2 + 3 + 4 + 5 + 6)",
                "E(X) = (1/6)(21)",
                "E(X) = 21/6 = 3.5"
            ],
            "final_answer": "3.5",
            "difficulty": "JEE_Main",
            "tags": ["probability", "expected value", "discrete distribution"],
            "topic": "Probability - Expected Value"
        },
        {
            "problem_id": "prob_005",
            "question": "In how many ways can 5 people be arranged in a row?",
            "solution_steps": [
                "This is a permutation problem",
                "Number of ways = 5!",
                "5! = 5 × 4 × 3 × 2 × 1",
                "5! = 120"
            ],
            "final_answer": "120 ways",
            "difficulty": "JEE_Main",
            "tags": ["probability", "permutations", "combinatorics", "counting"],
            "topic": "Probability - Combinatorics"
        },
        {
            "problem_id": "prob_006",
            "question": "How many 3-person committees can be formed from 7 people?",
            "solution_steps": [
                "This is a combination problem (order doesn't matter)",
                "Formula: C(n, k) = n!/(k!(n-k)!)",
                "C(7, 3) = 7!/(3!4!)",
                "= (7 × 6 × 5 × 4!)/(3! × 4!)",
                "= (7 × 6 × 5)/(3 × 2 × 1)",
                "= 210/6",
                "= 35"
            ],
            "final_answer": "35 committees",
            "difficulty": "JEE_Main",
            "tags": ["probability", "combinations", "combinatorics"],
            "topic": "Probability - Combinatorics"
        }
    ]
    
    for problem in probability_problems:
        kb.add_problem(**problem)
        problems_added += 1
        print(f"  ✓ Added {problem['problem_id']}: {problem['question'][:50]}...")
    
    # ==================== VECTORS PROBLEMS (3) ====================
    print("\n➡️ Adding VECTORS problems...")
    
    vector_problems = [
        {
            "problem_id": "vec_001",
            "question": "Find the dot product of vectors a = (3, 4) and b = (1, 2)",
            "solution_steps": [
                "Dot product formula: a·b = a₁b₁ + a₂b₂",
                "a·b = 3(1) + 4(2)",
                "a·b = 3 + 8",
                "a·b = 11"
            ],
            "final_answer": "11",
            "difficulty": "JEE_Main",
            "tags": ["vectors", "dot product", "inner product"],
            "topic": "Vectors - Operations"
        },
        {
            "problem_id": "vec_002",
            "question": "Find the cross product of vectors a = (1, 0, 0) and b = (0, 1, 0)",
            "solution_steps": [
                "Cross product formula: a × b = |i  j  k|",
                "                                |a₁ a₂ a₃|",
                "                                |b₁ b₂ b₃|",
                "a × b = |i  j  k|",
                "        |1  0  0|",
                "        |0  1  0|",
                "= i(0·0 - 0·1) - j(1·0 - 0·0) + k(1·1 - 0·0)",
                "= i(0) - j(0) + k(1)",
                "= (0, 0, 1) = k"
            ],
            "final_answer": "(0, 0, 1) or k",
            "difficulty": "JEE_Main",
            "tags": ["vectors", "cross product", "3d vectors"],
            "topic": "Vectors - Cross Product"
        },
        {
            "problem_id": "vec_003",
            "question": "Find the magnitude of vector v = (3, 4, 12)",
            "solution_steps": [
                "Magnitude formula: |v| = √(v₁² + v₂² + v₃²)",
                "|v| = √(3² + 4² + 12²)",
                "|v| = √(9 + 16 + 144)",
                "|v| = √169",
                "|v| = 13"
            ],
            "final_answer": "13",
            "difficulty": "JEE_Main",
            "tags": ["vectors", "magnitude", "norm"],
            "topic": "Vectors - Properties"
        }
    ]
    
    for problem in vector_problems:
        kb.add_problem(**problem)
        problems_added += 1
        print(f"  ✓ Added {problem['problem_id']}: {problem['question'][:50]}...")
    
    # ==================== COMPLEX NUMBERS PROBLEMS (2) ====================
    print("\n🔢 Adding COMPLEX NUMBERS problems...")
    
    complex_problems = [
        {
            "problem_id": "complex_001",
            "question": "Find the modulus and argument of z = 1 + i",
            "solution_steps": [
                "For z = a + bi, modulus |z| = √(a² + b²)",
                "|z| = √(1² + 1²) = √2",
                "Argument θ = arctan(b/a)",
                "θ = arctan(1/1) = arctan(1) = π/4 radians = 45°",
                "Since z is in first quadrant, arg(z) = π/4"
            ],
            "final_answer": "|z| = √2, arg(z) = π/4",
            "difficulty": "JEE_Main",
            "tags": ["complex numbers", "modulus", "argument", "polar form"],
            "topic": "Complex Numbers - Basic"
        },
        {
            "problem_id": "complex_002",
            "question": "Find (2 + 3i)(1 - 2i)",
            "solution_steps": [
                "Use FOIL method: (a + bi)(c + di) = ac + adi + bci + bdi²",
                "Remember i² = -1",
                "(2 + 3i)(1 - 2i) = 2(1) + 2(-2i) + 3i(1) + 3i(-2i)",
                "= 2 - 4i + 3i - 6i²",
                "= 2 - i - 6(-1)",
                "= 2 - i + 6",
                "= 8 - i"
            ],
            "final_answer": "8 - i",
            "difficulty": "JEE_Main",
            "tags": ["complex numbers", "multiplication", "operations"],
            "topic": "Complex Numbers - Operations"
        }
    ]
    
    for problem in complex_problems:
        kb.add_problem(**problem)
        problems_added += 1
        print(f"  ✓ Added {problem['problem_id']}: {problem['question'][:50]}...")
    
    # Final status
    final_count = kb.client.count(collection_name=kb.collection_name).count
    
    print("\n" + "=" * 70)
    print(f"  ✅ KNOWLEDGE BASE EXPANSION COMPLETE!")
    print("=" * 70)
    print(f"\nProblems added in this session: {problems_added}")
    print(f"Total KB size: {final_count} problems")
    print("\n📊 Topic Distribution:")
    print(f"  • Calculus: 16 problems")
    print(f"  • Algebra: 11 problems")
    print(f"  • Trigonometry: 6 problems")
    print(f"  • Geometry: 5 problems")
    print(f"  • Probability: 6 problems")
    print(f"  • Vectors: 3 problems")
    print(f"  • Complex Numbers: 2 problems")
    print(f"  • TOTAL: {final_count} problems ✅")
    print("\n✨ Knowledge base is now production-ready for JEE-level queries!")
    print("=" * 70)

if __name__ == "__main__":
    expand_knowledge_base()
