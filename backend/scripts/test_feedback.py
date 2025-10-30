"""
Test script for HITL Feedback System
Tests all feedback endpoints and functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_submit_positive_feedback():
    """Test submitting positive feedback"""
    print_section("TEST 1: Submit Positive Feedback")
    
    feedback_data = {
        "question": "Evaluate the integral of x² ln(x) from 0 to 1",
        "answer": "∫₀¹ x²ln(x)dx = (x³/3)ln(x) - x³/9 |₀¹ = -1/9",
        "rating": "thumbs_up",
        "comment": "Excellent step-by-step solution with clear explanation!",
        "metadata": {
            "source": "gemini_with_db",
            "confidence": "high",
            "confidence_score": 0.95,
            "problem_id": "calc_001"
        }
    }
    
    response = requests.post(f"{BASE_URL}/feedback/submit", json=feedback_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Positive feedback submitted successfully!")
        print(f"   Feedback ID: {result['feedback_id']}")
        print(f"   Message: {result['message']}")
        print(f"   Timestamp: {result['timestamp']}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_submit_negative_feedback_with_correction():
    """Test submitting negative feedback with correction"""
    print_section("TEST 2: Submit Negative Feedback with Correction")
    
    feedback_data = {
        "question": "Solve x³ - 3x + 2 = 0",
        "answer": "x = 1 (single root)",
        "rating": "thumbs_down",
        "correction": "x = 1 is correct, but also x = -2 (double root from factoring (x-1)(x+1)²=0)",
        "comment": "Missing one of the roots. Should show all solutions.",
        "metadata": {
            "source": "perplexity_web",
            "confidence": "medium"
        }
    }
    
    response = requests.post(f"{BASE_URL}/feedback/submit", json=feedback_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Negative feedback with correction submitted!")
        print(f"   Feedback ID: {result['feedback_id']}")
        print(f"   User correction: {feedback_data['correction'][:50]}...")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_submit_negative_feedback_not_found():
    """Test feedback for not found case"""
    print_section("TEST 3: Submit Feedback for Not Found Case")
    
    feedback_data = {
        "question": "What is the Cauchy-Schwarz inequality?",
        "answer": "I couldn't find information about this in my knowledge base.",
        "rating": "thumbs_down",
        "comment": "This is a fundamental theorem that should be in the knowledge base",
        "metadata": {
            "source": "not_found",
            "confidence": "none"
        }
    }
    
    response = requests.post(f"{BASE_URL}/feedback/submit", json=feedback_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Not found feedback submitted!")
        print(f"   Feedback ID: {result['feedback_id']}")
        print(f"   This will help identify knowledge base gaps")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_submit_multiple_positive():
    """Submit multiple positive feedback entries"""
    print_section("TEST 4: Submit Multiple Positive Feedback Entries")
    
    test_cases = [
        {
            "question": "Find the derivative of sin(x)cos(x)",
            "answer": "d/dx[sin(x)cos(x)] = cos²(x) - sin²(x) = cos(2x)",
            "rating": "thumbs_up",
            "comment": "Perfect! Used product rule correctly."
        },
        {
            "question": "What is the probability of getting exactly 2 red balls?",
            "answer": "P(X=2) = C(5,2) × (0.4)² × (0.6)³ = 0.3456",
            "rating": "thumbs_up",
            "comment": "Clear binomial probability calculation."
        },
        {
            "question": "Solve the quadratic equation x² + 5x + 6 = 0",
            "answer": "x = -2 or x = -3 (by factoring: (x+2)(x+3)=0)",
            "rating": "thumbs_up"
        }
    ]
    
    for i, feedback in enumerate(test_cases, 1):
        response = requests.post(f"{BASE_URL}/feedback/submit", json=feedback)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Positive feedback {i}/3: ID {result['feedback_id']}")
        else:
            print(f"❌ Failed {i}/3")

def test_get_statistics():
    """Test getting feedback statistics"""
    print_section("TEST 5: Get Feedback Statistics")
    
    response = requests.get(f"{BASE_URL}/feedback/stats")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Feedback Statistics Retrieved:")
        print(f"   Total Feedback: {stats['total_feedback']}")
        print(f"   Positive: {stats['positive']} ({stats['positive_rate']:.1%})")
        print(f"   Negative: {stats['negative']} ({stats['negative_rate']:.1%})")
        print(f"   With Corrections: {stats['with_corrections']} ({stats['correction_rate']:.1%})")
        
        # Performance assessment
        if stats['positive_rate'] >= 0.7:
            print(f"   📊 Performance: ✅ GOOD (≥70% positive)")
        elif stats['positive_rate'] >= 0.5:
            print(f"   📊 Performance: ⚠️ FAIR (50-70% positive)")
        else:
            print(f"   📊 Performance: ❌ NEEDS IMPROVEMENT (<50% positive)")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_get_improvements():
    """Test getting improvement suggestions"""
    print_section("TEST 6: Get AI Improvement Suggestions")
    
    response = requests.get(f"{BASE_URL}/feedback/improvements")
    
    if response.status_code == 200:
        improvements = response.json()
        print(f"✅ Improvement Suggestions Generated:")
        
        # Overall performance
        perf = improvements['overall_performance']
        print(f"\n   Overall Performance:")
        print(f"   • Status: {perf['status'].upper()}")
        print(f"   • Positive Rate: {perf['positive_rate']}")
        print(f"   • Total Feedback: {perf['total_feedback']}")
        
        # Priority actions
        if improvements['priority_actions']:
            print(f"\n   Priority Actions:")
            for i, action in enumerate(improvements['priority_actions'], 1):
                print(f"   {i}. [{action['priority'].upper()}] {action['type']}")
                print(f"      Reason: {action['reason']}")
                print(f"      Action: {action['action']}")
        else:
            print(f"\n   ✅ No priority actions needed - system performing well!")
        
        # Next steps
        if improvements['next_steps']:
            print(f"\n   Next Steps:")
            for i, step in enumerate(improvements['next_steps'], 1):
                print(f"   {i}. {step['action']}: {step['reason']}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_get_learning_report():
    """Test getting comprehensive learning report"""
    print_section("TEST 7: Get Comprehensive Learning Report")
    
    response = requests.get(f"{BASE_URL}/feedback/report")
    
    if response.status_code == 200:
        report = response.json()
        print(f"✅ Learning Report Generated:")
        
        # Statistics
        stats = report['statistics']
        print(f"\n   Statistics Summary:")
        print(f"   • Total: {stats['total_feedback']}")
        print(f"   • Positive: {stats['positive']} ({stats['positive_rate']:.1%})")
        print(f"   • Negative: {stats['negative']} ({stats['negative_rate']:.1%})")
        
        # Negative feedback analysis
        neg_analysis = report['negative_feedback_analysis']
        print(f"\n   Negative Feedback Analysis:")
        print(f"   • Total Negative: {neg_analysis['total']}")
        
        if neg_analysis['by_source']:
            print(f"   • By Source:")
            for source, count in neg_analysis['by_source'].items():
                print(f"     - {source}: {count}")
        
        if neg_analysis['by_topic']:
            print(f"   • By Topic:")
            for topic, count in neg_analysis['by_topic'].items():
                print(f"     - {topic}: {count}")
        
        print(f"\n   Report Timestamp: {report['timestamp']}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_list_feedback():
    """Test listing feedback entries"""
    print_section("TEST 8: List Recent Feedback")
    
    # List all feedback
    response = requests.get(f"{BASE_URL}/feedback/list?limit=5")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Listed {data['count']} recent feedback entries:\n")
        
        for i, fb in enumerate(data['feedback'], 1):
            print(f"   {i}. ID: {fb['id']} | Rating: {fb['rating']}")
            print(f"      Q: {fb['question'][:60]}...")
            print(f"      Timestamp: {fb['timestamp']}")
            if fb.get('comment'):
                print(f"      Comment: {fb['comment'][:50]}...")
            print()
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_list_by_rating():
    """Test listing feedback filtered by rating"""
    print_section("TEST 9: List Feedback by Rating")
    
    # Get only negative feedback
    response = requests.get(f"{BASE_URL}/feedback/list?rating=thumbs_down&limit=10")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['count']} negative feedback entries:")
        
        if data['count'] > 0:
            for fb in data['feedback']:
                print(f"\n   ID {fb['id']}: {fb['question'][:50]}...")
                if fb.get('correction'):
                    print(f"   ✏️ Correction: {fb['correction'][:60]}...")
                if fb.get('comment'):
                    print(f"   💬 Comment: {fb['comment'][:60]}...")
        else:
            print(f"   🎉 No negative feedback - excellent performance!")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def test_invalid_rating():
    """Test error handling for invalid rating"""
    print_section("TEST 10: Error Handling - Invalid Rating")
    
    feedback_data = {
        "question": "Test question",
        "answer": "Test answer",
        "rating": "invalid_rating"  # Should fail validation
    }
    
    response = requests.post(f"{BASE_URL}/feedback/submit", json=feedback_data)
    
    if response.status_code == 400:
        print(f"✅ Correctly rejected invalid rating")
        print(f"   Error: {response.json()['detail']}")
    else:
        print(f"❌ Expected 400 error, got: {response.status_code}")

def run_all_tests():
    """Run all HITL feedback system tests"""
    print("\n" + "="*60)
    print("  HITL FEEDBACK SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Target: {BASE_URL}")
    print("="*60)
    
    tests = [
        test_submit_positive_feedback,
        test_submit_negative_feedback_with_correction,
        test_submit_negative_feedback_not_found,
        test_submit_multiple_positive,
        test_get_statistics,
        test_get_improvements,
        test_get_learning_report,
        test_list_feedback,
        test_list_by_rating,
        test_invalid_rating
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            failed += 1
    
    print_section("TEST SUMMARY")
    print(f"   Total Tests: {len(tests)}")
    print(f"   Passed: ✅ {passed}")
    print(f"   Failed: ❌ {failed}")
    print(f"   Success Rate: {(passed/len(tests)*100):.1f}%")
    
    if failed == 0:
        print(f"\n   🎉 ALL TESTS PASSED! HITL SYSTEM FULLY OPERATIONAL!")
    else:
        print(f"\n   ⚠️ Some tests failed. Check backend logs for details.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        # Check if backend is running
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Backend server is running at {BASE_URL}")
    except requests.ConnectionError:
        print(f"❌ ERROR: Backend server is not running at {BASE_URL}")
        print(f"   Please start the backend server first:")
        print(f"   cd backend && uvicorn app.main:app --reload")
        exit(1)
    
    run_all_tests()
