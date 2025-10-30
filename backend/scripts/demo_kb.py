"""
Demo script to show Knowledge Base in action
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vector_db import MathKnowledgeBase

print("=" * 70)
print("  KNOWLEDGE BASE DEMONSTRATION")
print("=" * 70)

# Initialize KB
kb = MathKnowledgeBase()

# Check current size
count = kb.client.count(collection_name=kb.collection_name).count
print(f"\n📚 Total problems in Knowledge Base: {count}")

# Add sample problems if empty
if count == 0:
    print("\nℹ️  Knowledge Base is empty. Adding sample problems...")
    from scripts.populate_kb import populate_kb
    populate_kb()
    count = kb.client.count(collection_name=kb.collection_name).count
    print(f"✅ Added problems. New total: {count}")

print("\n" + "=" * 70)
print("  SEMANTIC SEARCH DEMONSTRATION")
print("=" * 70)

# Test queries
test_queries = [
    "solve cubic polynomial",
    "integration by parts",
    "find derivative"
]

for query in test_queries:
    print(f"\n🔍 Query: '{query}'")
    print("-" * 70)
    
    results = kb.search_similar(query, top_k=2, score_threshold=0.3)
    
    if results:
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. Problem ID: {result['problem_id']}")
            print(f"     Similarity: {result['score']:.1%}")
            print(f"     Question: {result['question'][:60]}...")
            print(f"     Topic: {result['topic']}")
    else:
        print("  ❌ No matches found")

print("\n" + "=" * 70)
print("  KEY INSIGHTS")
print("=" * 70)
print("""
✅ Qdrant converts questions to 384-dimensional vectors
✅ Finds similar problems by comparing vector similarity
✅ Works even when exact words don't match
✅ Returns confidence scores (0-100%)
✅ Top matches used to generate step-by-step solutions
""")
