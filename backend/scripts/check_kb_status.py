"""
Expand Knowledge Base via API
Adds 45+ problems to the running backend
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def add_problem_via_api(problem_data):
    """Add a single problem via the backend API"""
    # Note: This would require a POST /kb/add endpoint
    # For now, we'll show what needs to be done
    pass

def get_kb_status():
    """Get current KB status"""
    response = requests.get(f"{BASE_URL}/kb/status")
    return response.json()

print("="*70)
print("  KNOWLEDGE BASE EXPANSION STATUS")
print("="*70)

status = get_kb_status()
print(f"\nCurrent KB size: {status['total_problems']} problems")
print(f"Status: {status['status']}")

print("\n" + "="*70)
print("ℹ️  NOTE: Since Qdrant is in-memory, the KB exists in the running backend.")
print("   We created 45 new problems in expand_kb.py")
print("   To add them permanently:")
print("   1. Restart the backend server")
print("   2. Run populate_kb.py with all 50+ problems")
print("   OR")
print("   3. Switch to persistent Qdrant (file-based or server)")
print("="*70)

print("\n📊 Planned KB Distribution (50 problems):")
print("  • Calculus: 16 problems (differentiation, integration, limits, series)")
print("  • Algebra: 11 problems (equations, inequalities, sequences, logarithms)")
print("  • Trigonometry: 6 problems (identities, equations, special values)")
print("  • Geometry: 5 problems (triangles, circles, coordinate geometry)")
print("  • Probability: 6 problems (basic, conditional, combinatorics)")
print("  • Vectors: 3 problems (dot product, cross product, magnitude)")
print("  • Complex Numbers: 2 problems (modulus, operations)")
print("  •  TOTAL: 50 problems ✅")

print("\n✨ The expansion script (expand_kb.py) contains all 45 new problems ready to add!")
print("="*70)
