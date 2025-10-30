"""
View User Feedback and Problem Reports
Simple terminal viewer for feedback.json
"""

import json
import os
from datetime import datetime
from typing import List, Dict

def load_feedback() -> List[Dict]:
    """Load feedback from JSON file"""
    feedback_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'feedback.json')
    
    if not os.path.exists(feedback_file):
        print("❌ No feedback file found!")
        return []
    
    with open(feedback_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_stats(feedback: List[Dict]):
    """Print feedback statistics"""
    total = len(feedback)
    positive = len([f for f in feedback if f['rating'] == 'thumbs_up'])
    negative = len([f for f in feedback if f['rating'] == 'thumbs_down'])
    problem_reports = len([f for f in feedback if f.get('feedback_type') == 'problem_report'])
    with_corrections = len([f for f in feedback if f.get('correction', '').strip()])
    
    print("\n" + "=" * 80)
    print("📊 FEEDBACK STATISTICS")
    print("=" * 80)
    print(f"📋 Total Feedback:        {total}")
    print(f"👍 Positive:              {positive} ({positive/total*100:.1f}% if total else 0)")
    print(f"👎 Negative:              {negative} ({negative/total*100:.1f}% if total else 0)")
    print(f"🐛 Problem Reports:       {problem_reports}")
    print(f"✏️  With Corrections:      {with_corrections}")
    print("=" * 80 + "\n")

def print_feedback_item(fb: Dict, show_full: bool = False):
    """Print a single feedback item"""
    print("-" * 80)
    print(f"📌 Feedback #{fb['id']}")
    print(f"📅 Date: {fb['timestamp']}")
    
    # Rating badge
    if fb['rating'] == 'thumbs_up':
        print(f"✅ Rating: 👍 POSITIVE")
    else:
        print(f"❌ Rating: 👎 NEGATIVE")
    
    # Problem report info
    if fb.get('feedback_type') == 'problem_report':
        print(f"🐛 TYPE: PROBLEM REPORT")
        if fb.get('metadata', {}).get('problem_type'):
            prob_type = fb['metadata']['problem_type'].upper().replace('_', ' ')
            icons = {
                'BUG': '🐛',
                'FEATURE': '💡',
                'IMPROVEMENT': '⚡',
                'OCR': '📷',
                'WRONG ANSWER': '❌',
                'OTHER': '📋'
            }
            icon = icons.get(prob_type, '📋')
            print(f"   Category: {icon} {prob_type}")
        
        if fb.get('metadata', {}).get('user_email'):
            print(f"   📧 Email: {fb['metadata']['user_email']}")
    
    print(f"\n❓ Question:")
    print(f"   {fb['question'][:200]}{'...' if len(fb['question']) > 200 else ''}")
    
    if fb.get('answer'):
        print(f"\n💡 Answer:")
        answer = fb['answer'][:300] + '...' if len(fb['answer']) > 300 else fb['answer']
        print(f"   {answer}")
    
    if fb.get('comment'):
        print(f"\n💬 Comment:")
        print(f"   {fb['comment']}")
    
    if fb.get('correction'):
        print(f"\n✏️  User Correction:")
        print(f"   {fb['correction']}")
    
    # Metadata
    if fb.get('metadata', {}).get('source'):
        print(f"\n🔍 Source: {fb['metadata']['source']}")
    if fb.get('metadata', {}).get('confidence'):
        print(f"   Confidence: {fb['metadata']['confidence']}")
    
    print("-" * 80 + "\n")

def view_all(feedback: List[Dict]):
    """View all feedback"""
    print_stats(feedback)
    print("\n📋 ALL FEEDBACK:\n")
    for fb in reversed(feedback):  # Newest first
        print_feedback_item(fb)

def view_positive(feedback: List[Dict]):
    """View positive feedback"""
    positive = [f for f in feedback if f['rating'] == 'thumbs_up']
    print(f"\n👍 POSITIVE FEEDBACK ({len(positive)} items):\n")
    for fb in reversed(positive):
        print_feedback_item(fb)

def view_negative(feedback: List[Dict]):
    """View negative feedback"""
    negative = [f for f in feedback if f['rating'] == 'thumbs_down']
    print(f"\n👎 NEGATIVE FEEDBACK ({len(negative)} items):\n")
    for fb in reversed(negative):
        print_feedback_item(fb)

def view_problem_reports(feedback: List[Dict]):
    """View problem reports"""
    problems = [f for f in feedback if f.get('feedback_type') == 'problem_report']
    print(f"\n🐛 PROBLEM REPORTS ({len(problems)} items):\n")
    
    if not problems:
        print("   No problem reports yet!\n")
        return
    
    for fb in reversed(problems):
        print_feedback_item(fb)

def view_with_corrections(feedback: List[Dict]):
    """View feedback with corrections"""
    corrections = [f for f in feedback if f.get('correction', '').strip()]
    print(f"\n✏️  FEEDBACK WITH CORRECTIONS ({len(corrections)} items):\n")
    for fb in reversed(corrections):
        print_feedback_item(fb)

def main():
    """Main function"""
    feedback = load_feedback()
    
    if not feedback:
        print("\n📭 No feedback available yet!\n")
        return
    
    while True:
        print("\n" + "=" * 80)
        print("📊 USER FEEDBACK & PROBLEM REPORTS VIEWER")
        print("=" * 80)
        print("\nOptions:")
        print("  1. 📊 View Statistics")
        print("  2. 📋 View All Feedback")
        print("  3. 👍 View Positive Feedback")
        print("  4. 👎 View Negative Feedback")
        print("  5. 🐛 View Problem Reports")
        print("  6. ✏️  View Feedback with Corrections")
        print("  7. 🔄 Refresh Data")
        print("  0. ❌ Exit")
        print("\n" + "-" * 80)
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!\n")
            break
        elif choice == '1':
            print_stats(feedback)
        elif choice == '2':
            view_all(feedback)
        elif choice == '3':
            view_positive(feedback)
        elif choice == '4':
            view_negative(feedback)
        elif choice == '5':
            view_problem_reports(feedback)
        elif choice == '6':
            view_with_corrections(feedback)
        elif choice == '7':
            feedback = load_feedback()
            print("\n✅ Data refreshed!\n")
        else:
            print("\n❌ Invalid choice! Please try again.\n")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
