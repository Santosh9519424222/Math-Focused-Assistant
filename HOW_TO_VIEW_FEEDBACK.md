# 📊 How to View User Feedback & Problem Reports

## 🎯 3 Ways to View Feedback

---

## **Option 1: Web Dashboard** (Recommended ⭐)

### **Beautiful Visual Interface**

1. **Start your backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

2. **Open the dashboard:**
```bash
# Double-click this file:
backend/view_feedback.html

# Or open in browser:
file:///C:/Users/Lenovo/OneDrive/Desktop/new%20chatbot/backend/view_feedback.html
```

### **Features:**
- ✅ Real-time statistics (Total, Positive, Negative, Problems)
- ✅ Filter by type (All, Positive, Negative, Problem Reports, Corrections)
- ✅ Color-coded cards
- ✅ Auto-refresh every 30 seconds
- ✅ Beautiful gradient design
- ✅ Mobile responsive

### **Screenshot:**
```
┌─────────────────────────────────────────┐
│ 📊 User Feedback & Problem Reports      │
├─────────────────────────────────────────┤
│  📋 Total: 12  | 👍 8 | 👎 4 | 🐛 2    │
├─────────────────────────────────────────┤
│ [📋 All] [👍 Positive] [👎 Negative]   │
│ [🐛 Problem Reports] [✏️ Corrections]   │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Feedback #12        👍 Positive  │   │
│  │ 📅 2025-10-30 16:30:00          │   │
│  │                                  │   │
│  │ Question: How to solve...       │   │
│  │ Answer: Step-by-step...         │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Feedback #11    🐛 Problem Report│   │
│  │ 📅 2025-10-30 16:25:00          │   │
│  │ 📷 OCR ISSUE                     │   │
│  │ 📧 user@example.com             │   │
│  │                                  │   │
│  │ Description: OCR not reading... │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## **Option 2: Terminal Viewer** (Quick Access)

### **Interactive Command-Line Interface**

1. **Run the viewer:**
```bash
cd backend
python scripts/view_feedback.py
```

2. **Menu options:**
```
📊 USER FEEDBACK & PROBLEM REPORTS VIEWER
════════════════════════════════════════
Options:
  1. 📊 View Statistics
  2. 📋 View All Feedback
  3. 👍 View Positive Feedback
  4. 👎 View Negative Feedback
  5. 🐛 View Problem Reports
  6. ✏️ View Feedback with Corrections
  7. 🔄 Refresh Data
  0. ❌ Exit

Enter your choice (0-7): 
```

### **Example Output:**
```
📊 FEEDBACK STATISTICS
════════════════════════════════════════
📋 Total Feedback:        12
👍 Positive:              8 (66.7%)
👎 Negative:              4 (33.3%)
🐛 Problem Reports:       2
✏️ With Corrections:      3
════════════════════════════════════════

────────────────────────────────────────
📌 Feedback #12
📅 Date: 2025-10-30T16:30:00
✅ Rating: 👍 POSITIVE

❓ Question:
   How to solve quadratic equations?

💡 Answer:
   Step-by-step solution...

🔍 Source: gemini_with_db
   Confidence: high
────────────────────────────────────────
```

---

## **Option 3: Direct File Access** (Simple)

### **JSON File Inspection**

1. **Location:**
```
backend/data/feedback.json
```

2. **Open in VS Code:**
```bash
code backend/data/feedback.json
```

3. **Or view in terminal:**
```bash
# Windows PowerShell
Get-Content backend/data/feedback.json | ConvertFrom-Json | Format-List

# Or simply
cat backend/data/feedback.json
```

### **Example Entry:**
```json
{
  "id": 12,
  "timestamp": "2025-10-30T16:30:00.123456",
  "question": "How to solve x² + 5x + 6 = 0?",
  "answer": "Step-by-step solution...",
  "rating": "thumbs_up",
  "feedback_type": "answer_feedback",
  "comment": "Very helpful!",
  "correction": "",
  "metadata": {
    "source": "gemini_with_db",
    "confidence": "high",
    "problem_id": "alg_001"
  }
}
```

---

## 🔍 Finding Specific Feedback Types

### **Problem Reports Only:**
```json
// Look for entries with:
{
  "feedback_type": "problem_report",
  "metadata": {
    "source": "user_problem_report",
    "problem_type": "bug|feature|improvement|ocr|wrong_answer|other",
    "user_email": "user@example.com"  // if provided
  }
}
```

### **Filter Commands:**

**Web Dashboard:**
- Click "🐛 Problem Reports" button

**Terminal Viewer:**
- Choose option 5

**JSON File:**
```bash
# Search for problem reports
cat backend/data/feedback.json | grep "problem_report"

# Or use Python
python -c "import json; data=json.load(open('backend/data/feedback.json')); print([f for f in data if f.get('feedback_type')=='problem_report'])"
```

---

## 📊 Understanding Feedback Types

### **1. Positive Feedback (👍)**
```json
{
  "rating": "thumbs_up",
  "feedback_type": "answer_feedback",
  "comment": "Great explanation!",
  "metadata": {
    "source": "gemini_with_db"
  }
}
```

### **2. Negative Feedback (👎)**
```json
{
  "rating": "thumbs_down",
  "feedback_type": "answer_feedback",
  "comment": "Wrong answer",
  "correction": "The correct answer is x = 5",
  "metadata": {
    "source": "perplexity_web"
  }
}
```

### **3. Problem Report (🐛)**
```json
{
  "question": "[USER PROBLEM REPORT - BUG]",
  "rating": "thumbs_down",
  "feedback_type": "problem_report",
  "comment": "Type: ocr\nEmail: user@example.com\n\nDescription: OCR not working",
  "metadata": {
    "source": "user_problem_report",
    "problem_type": "ocr",
    "user_email": "user@example.com"
  }
}
```

---

## 🎯 Quick Access Summary

| Method | Best For | Access |
|--------|----------|--------|
| **Web Dashboard** | Visual browsing, statistics | Open `view_feedback.html` |
| **Terminal Viewer** | Quick checks, filtering | `python scripts/view_feedback.py` |
| **JSON File** | Raw data, scripting | Open `data/feedback.json` |

---

## 📈 Monitoring Workflow

### **Daily Routine:**

1. **Morning Check:**
```bash
# Quick stats
python scripts/view_feedback.py
# Choose option 1 (Statistics)
```

2. **Review Problem Reports:**
```bash
# View all problem reports
python scripts/view_feedback.py
# Choose option 5 (Problem Reports)
```

3. **Check Corrections:**
```bash
# See user corrections
python scripts/view_feedback.py
# Choose option 6 (With Corrections)
```

4. **Web Dashboard (Deep Dive):**
```
Open view_feedback.html
Filter by type
Review each item
Take notes on issues
```

---

## 🔔 Notification System (Optional)

### **Get Email Alerts:**

Create `backend/scripts/email_alerts.py`:
```python
import json
import smtplib
from email.message import EmailMessage

def check_new_problems():
    with open('../data/feedback.json') as f:
        feedback = json.load(f)
    
    recent_problems = [
        f for f in feedback 
        if f.get('feedback_type') == 'problem_report'
        # Add time filter for "today"
    ]
    
    if recent_problems:
        send_email_alert(recent_problems)

# Add email sending logic...
```

---

## 📊 Export Options

### **Export to CSV:**
```python
import json
import csv

with open('data/feedback.json') as f:
    feedback = json.load(f)

with open('feedback_export.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'timestamp', 'rating', 'question', 'comment'])
    writer.writeheader()
    for fb in feedback:
        writer.writerow({
            'id': fb['id'],
            'timestamp': fb['timestamp'],
            'rating': fb['rating'],
            'question': fb['question'],
            'comment': fb.get('comment', '')
        })
```

---

## 🎯 Action Items from Feedback

### **Priority System:**

**🔴 HIGH PRIORITY (Act within 24h):**
- Bug reports
- Wrong answer reports
- System errors

**🟡 MEDIUM PRIORITY (Act within 1 week):**
- OCR issues
- Improvement suggestions
- Multiple negative feedback on same topic

**🟢 LOW PRIORITY (Review monthly):**
- Feature requests
- General feedback
- Other category

---

## ✅ Summary

You now have **3 easy ways** to view all user feedback and problem reports:

1. **🌐 Web Dashboard** - `view_feedback.html` (Beautiful UI)
2. **💻 Terminal Viewer** - `scripts/view_feedback.py` (Quick access)
3. **📄 JSON File** - `data/feedback.json` (Raw data)

**All feedback is automatically saved** when users:
- Click 👍 or 👎 on answers
- Submit problem reports via the floating button
- Provide corrections or comments

**Start monitoring now!** 🚀

---

*Last Updated: October 30, 2025*
