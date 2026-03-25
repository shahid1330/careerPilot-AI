# 🧪 COMPLETE TESTING GUIDE - CareerPilot AI Phase 6A & 6B

**Project:** CareerPilot AI - Smart Mock Test & Career Intelligence System  
**Date:** 2026-02-27  
**Status:** 100% COMPLETE ✅

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Testing Phase 6A - Mock Test System](#testing-phase-6a---mock-test-system)
4. [Testing Phase 6B - Career Intelligence](#testing-phase-6b---career-intelligence)
5. [Testing Anti-Cheat System](#testing-anti-cheat-system)
6. [Testing Performance Dashboard](#testing-performance-dashboard)
7. [Common Issues & Solutions](#common-issues--solutions)
8. [API Testing](#api-testing)

---

## 🔧 PREREQUISITES

### Required Software:
- ✅ Python 3.11+
- ✅ Node.js 18+ & npm
- ✅ PostgreSQL 14+
- ✅ Git

### Environment Setup:
```bash
# Backend dependencies
python, fastapi, sqlalchemy, pydantic, groq, anthropic

# Frontend dependencies
Next.js 14, React 18, TailwindCSS, Framer Motion, Monaco Editor
```

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Clone & Install

```bash
# Navigate to project
cd "e:\Christ University\Trimester 6\Project"

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Step 2: Database Setup

```bash
cd backend

# Apply migrations
alembic upgrade head

# Seed daily quotes
python populate_daily_quotes.py
```

### Step 3: Start Services

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Step 4: Verify Services

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## 🧪 TESTING PHASE 6A - MOCK TEST SYSTEM

### Test 1: User Authentication & Setup

**Steps:**
1. Navigate to http://localhost:3000
2. Click "Login" or "Sign Up"
3. Create account or login:
   - Email: test@example.com
   - Password: Test123!
4. Verify redirect to dashboard

**Expected Result:** ✅ Successfully logged in, dashboard loads

---

### Test 2: Roadmap Creation

**Steps:**
1. From dashboard, click "Roadmap"
2. Fill in details:
   - **Role:** Python Developer
   - **Experience:** Beginner
   - **Duration:** 90 days
3. Click "Generate Personalized Roadmap"
4. Wait for AI to generate roadmap (10-30 seconds)

**Expected Result:** ✅ Roadmap generated with topics, milestones, weeks

---

### Test 3: Daily Plan Completion

**Steps:**
1. Click "Daily Plan" from sidebar
2. See list of days with topics
3. **Complete at least 5 days:**
   - Click the checkbox next to each day
   - Watch status change to "Completed"
   - Green checkmark appears
4. Verify "Available for Mock Tests: Yes"

**Expected Result:** ✅ At least 5 days marked complete, eligible for tests

---

### Test 4: Mock Test Generation

**Steps:**
1. Click "Mock Tests" from sidebar
2. Click "Generate New Test" button
3. **Configure test:**
   - MCQ Count: Select 15 (10/15/20)
   - Coding Count: Select 3 (2/3/4)
4. Click "Generate Test & Start"
5. Wait 10-20 seconds for AI generation

**Expected Result:** ✅ Test generated with:
- MCQ questions from completed topics ONLY
- Coding questions with visible test cases
- Confirmation modal appears

---

### Test 5: Fullscreen & Anti-Cheat Modal

**Steps:**
1. After test generation, see confirmation modal
2. **Read the rules:**
   - Fullscreen enforcement
   - Tab switching tracked
   - Copy/paste disabled
   - Right-click disabled
   - 7+ violations = auto-submit
3. Click "I Understand - Start Test"
4. Browser enters fullscreen (if supported)

**Expected Result:** ✅ Modal shows rules, fullscreen activates

---

### Test 6: MCQ Section - Sidebar Navigation

**Steps:**
1. **Left sidebar should show:**
   - Section 1: MCQ (grid of numbered buttons)
   - Section 2: Coding (card-style buttons)
   - Progress bar at bottom
2. **Click question number "3" in sidebar**
   - Question 3 loads immediately
   - Button turns BLUE (current)
3. **Answer question 3:**
   - Select option B
   - Button turns GREEN with checkmark
4. **Click question "1":**
   - Jump to question 1
   - Previously answered question 3 stays GREEN

**Expected Result:** ✅ Sidebar navigation works, colors correct

---

### Test 7: MCQ Section - Answer Questions

**Steps:**
1. For each MCQ question:
   - Read question text
   - See 4 options (A, B, C, D)
   - Select one option
   - See selection highlighted in BLUE
   - Question number turns GREEN in sidebar
2. Navigate using:
   - Sidebar (click any number)
   - OR "Previous" / "Next" buttons at bottom

**Expected Result:** ✅ All 15 MCQs answerable, navigation smooth

---

### Test 8: Coding Section - Monaco Editor

**Steps:**
1. Navigate to coding section (click "Problem 1" in sidebar)
2. **Verify Monaco Editor loads:**
   - Dark theme
   - Syntax highlighting
   - Line numbers
   - Auto-complete
3. **Language Badge:**
   - Should show "PYTHON" (for Python Developer role)
   - NOT changeable (locked to role)
4. **Write simple code:**
   ```python
   def solution(arr):
       return sum(arr)
   ```

**Expected Result:** ✅ Editor works, language locked, code editable

---

### Test 9: RUN CODE Button (Visible Test Cases)

**Steps:**
1. In coding question, write a solution
2. Click "Run Code" button (GREEN)
3. **Verify execution:**
   - Button shows "Running..."
   - After 1-2 seconds, results appear
4. **Check results card:**
   - Shows status (Accepted / Wrong Answer)
   - Shows "2 / 3 test cases passed" (example)
   - Shows runtime and memory
   - Shows DETAILED input/output for VISIBLE cases only
5. **Try clicking "Run Code" multiple times**
   - Should work every time (no limit)

**Expected Result:** ✅ Runs visible cases only, can run unlimited times

---

### Test 10: SUBMIT SOLUTION Button (All Test Cases)

**Steps:**
1. Write correct solution
2. Click "Submit Solution" button (BLUE)
3. **Confirmation dialog appears:**
   - "Submit this solution?"
   - "This will run ALL test cases (including hidden ones)"
   - "You can only submit once per question"
4. Click "OK"
5. **Verify execution:**
   - Runs ALL test cases (50-100 cases)
   - Takes 3-10 seconds
   - Shows status: "Accepted" or "Wrong Answer"
   - Shows "48 / 50 test cases passed" (example)
   - Hidden test cases show "Hidden" for input/output
6. **Try clicking "Submit Solution" again:**
   - Button is DISABLED
   - Shows "Submitted" badge

**Expected Result:** ✅ Runs all cases, can only submit once, hidden cases protected

---

### Test 11: Anti-Cheat Violation Testing

**Steps:**
1. While test is running, try these actions:
   - **Switch tabs** (Alt+Tab or Ctrl+Tab)
     - Violation logged
   - **Exit fullscreen** (Esc key)
     - Violation logged, warning shown
   - **Right-click** on question text
     - Disabled, violation logged
   - **Copy question text** (Ctrl+C)
     - Disabled, violation logged
2. **Check sidebar:**
   - Violations count increases
   - "3 Violations" shown in red box
3. **At 3 violations:**
   - Alert: "WARNING: 3 violations detected..."
4. **At 5 violations:**
   - Alert: "WARNING: 5 violations detected..."
5. **At 7+ violations:**
   - Alert: "Too many violations. Test will be auto-submitted."
   - Test auto-submits

**Expected Result:** ✅ Violations tracked, warnings shown, auto-submit at 7+

---

### Test 12: Timer & Auto-Submit

**Steps:**
1. **Check timer:**
   - Top-right corner shows: "02:00:00" (2 hours)
   - Counts down every second
2. **When timer < 10 minutes:**
   - Timer turns RED
   - Shows: "⚠️ Less than 10 minutes left!"
   - Pulse animation
3. **When timer reaches 0:**
   - Alert: "Time's up! Submitting automatically..."
   - Test auto-submits
   - Redirects to results page

**Expected Result:** ✅ Timer counts down, auto-submits at 0

---

### Test 13: Manual Test Submission

**Steps:**
1. Navigate to last coding question
2. Click "Submit Test" button at bottom
3. **Confirmation dialog:**
   - "Are you sure you want to submit?"
   - "You cannot change answers after submission"
4. Click "OK"
5. **Verify submission:**
   - Exits fullscreen
   - Shows loading: "Submitting Test..."
   - Redirects to results page

**Expected Result:** ✅ Test submits successfully, shows results

---

### Test 14: Test Results Page

**Steps:**
1. After submission, see results page
2. **Verify displayed data:**
   - Total score (%)
   - MCQ score (e.g., "12 / 15 correct")
   - Coding score (e.g., "2 / 3 passed")
   - Time taken
   - Violations count
3. **Sections:**
   - MCQ breakdown (question by question)
   - Coding breakdown (test cases passed)
   - Strong topics (topics you did well)
   - Weak topics (topics to improve)
4. **AI feedback:**
   - Personalized improvement suggestions
   - Next steps

**Expected Result:** ✅ Complete results shown with AI feedback

---

## 🧠 TESTING PHASE 6B - CAREER INTELLIGENCE

### Test 15: Career Intelligence Dashboard

**Steps:**
1. **Complete 3+ mock tests first** (required for data)
2. Click "Career Intelligence" from sidebar
3. Wait for loading (analyzing data)

**If no data:**
- Shows: "Build Your Career Profile"
- "Complete at least 3 mock tests to unlock..."
- Button: "Take Mock Test"

**If data available:**

---

### Test 16: Career DNA Profile

**Steps:**
1. See "Your Career DNA" section
2. **Verify 5 dimensions:**
   - Logical Ability (%)
   - Problem Solving (%)
   - Speed (%)
   - Consistency (%)
   - Learning Efficiency (%)
3. Each shows:
   - Icon
   - Score (0-100%)
   - Progress bar
   - Label (Excellent/Good/Average/Needs Improvement)
4. **Overall Career Readiness Score:**
   - Large card at bottom
   - Shows overall % (average of 5 dimensions)

**Expected Result:** ✅ All dimensions calculated from test performance

---

### Test 17: Skill Mastery Map

**Steps:**
1. See "Skill Mastery Map" section
2. **Verify skills displayed:**
   - Each skill is a card
   - Shows skill name (e.g., "Python", "Data Structures")
   - Shows category tag (e.g., "programming")
   - Shows mastery % (0-100%)
   - Progress bar
3. **Skills are derived from:**
   - Test performance
   - Topics practiced
   - Accuracy per topic

**Expected Result:** ✅ Skills shown with mastery levels

---

### Test 18: Career Forecast

**Steps:**
1. See "Career Forecast" section
2. **Verify forecasts:**
   - **Internship Readiness:** % with progress bar
   - **Placement Readiness:** % with progress bar
   - **Best-Fit Roles:** List of recommended roles
   - **Estimated Timeline:** "2-3 months" etc.
3. **Roles should match user's roadmap:**
   - Python Developer → Python Engineer, Backend Developer
   - Java Developer → Java Developer, Android Developer

**Expected Result:** ✅ Forecasts based on performance

---

### Test 19: Weekly Learning Strategy

**Steps:**
1. See "Your Weekly Learning Strategy" section
2. **Verify 3 components:**
   - **Focus Topics:** 3-5 topics to concentrate on
   - **Practice Hours:** Recommended hours per week
   - **Improvement Areas:** 3-5 weak topics
3. All derived from weak areas in tests

**Expected Result:** ✅ Personalized strategy shown

---

### Test 20: AI Coach Insights

**Steps:**
1. See "AI Coach Insights" section (purple background)
2. **Verify insights:**
   - 3-5 personalized insights
   - Based on test patterns
   - Actionable advice
3. Example insights:
   - "Your consistency has improved by 15% this week"
   - "Focus on Data Structures - 60% accuracy"
   - "You solve easy problems faster than average"

**Expected Result:** ✅ AI-generated personalized insights

---

## 📊 TESTING PERFORMANCE DASHBOARD

### Test 21: Performance Analytics

**Steps:**
1. Click "Performance" from sidebar
2. **Verify sections:**
   - **Key Metrics Cards:**
     - Tests Completed
     - Average Score
     - Best Score
     - Improvement %
   - **Score Trend Graph:**
     - Last 10 tests
     - Line chart showing scores over time
   - **Strong Areas:**
     - Topics with > 70% accuracy
     - Green cards
   - **Weak Areas:**
     - Topics with < 70% accuracy
     - Orange cards
     - "Practice Now" buttons
   - **AI-Powered Recommendations:**
     - Personalized tips per weak topic
   - **Daily Quote:**
     - Motivational quote at top

**Expected Result:** ✅ Complete performance overview

---

## 🐛 COMMON ISSUES & SOLUTIONS

### Issue 1: "No completed topics" error

**Solution:**
- Go to Daily Plan
- Complete at least 5 days
- Check "Available for Mock Tests" shows "Yes"

---

### Issue 2: Test generation fails

**Solutions:**
- Check backend console for errors
- Verify GROQ_API_KEY is set in .env
- Check database connection
- Run: `alembic upgrade head`

---

### Issue 3: Fullscreen doesn't work

**Solution:**
- This is browser-dependent
- Chrome/Edge: Works perfectly
- Firefox: May need permission
- Safari: Limited support
- **Test still works without fullscreen**

---

### Issue 4: Monaco Editor doesn't load

**Solutions:**
- Clear browser cache
- Check browser console for errors
- Verify internet connection (CDN dependency)
- Try different browser

---

### Issue 5: Coding execution fails

**Solutions:**
- Check Python is installed: `python --version`
- For Java: Install JDK 11+
- For JavaScript: Install Node.js
- Check backend logs for detailed errors

---

### Issue 6: No Career Intelligence data

**Solution:**
- Complete at least 3 mock tests
- Wait 30 seconds after last test
- Refresh Career Intelligence page

---

## 🔌 API TESTING

### Test APIs with curl or Postman:

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Save token from response

# Generate Mock Test
curl -X POST http://localhost:8000/api/mock-tests/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_role_id":1,"mcq_count":15,"coding_count":3}'

# Get Test
curl http://localhost:8000/api/mock-tests/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Run Code (visible only)
curl -X POST http://localhost:8000/api/execute/run-code \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question_id":1,"code":"def solution(arr):\n    return sum(arr)","language":"python","visible_only":true}'

# Submit Code (all test cases)
curl -X POST http://localhost:8000/api/execute/submit-code \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question_id":1,"code":"def solution(arr):\n    return sum(arr)","language":"python","visible_only":false}'

# Get Career Intelligence
curl http://localhost:8000/api/career-intelligence/profile?user_role_id=1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Performance Summary
curl http://localhost:8000/api/performance/summary?user_role_id=1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Daily Quote
curl http://localhost:8000/api/daily-quote
```

---

## ✅ TESTING CHECKLIST

Use this checklist while testing:

### Authentication & Setup
- [ ] Sign up works
- [ ] Login works
- [ ] Dashboard loads
- [ ] Sidebar navigation works

### Roadmap & Daily Plan
- [ ] Roadmap generates
- [ ] Daily plan shows days
- [ ] Can mark days complete
- [ ] Eligible for tests after 5 days

### Mock Test Generation
- [ ] Test generates from completed topics only
- [ ] MCQ questions appear
- [ ] Coding questions appear
- [ ] Confirmation modal shows

### Fullscreen & Anti-Cheat
- [ ] Fullscreen activates
- [ ] Tab switch tracked
- [ ] Fullscreen exit tracked
- [ ] Right-click disabled
- [ ] Copy/paste disabled (except editor)
- [ ] Violations shown in sidebar
- [ ] Auto-submit at 7+ violations

### MCQ Section
- [ ] Sidebar shows all MCQ numbers
- [ ] Click number to jump
- [ ] Answered questions turn green
- [ ] Current question turns blue
- [ ] Progress bar updates

### Coding Section
- [ ] Monaco Editor loads
- [ ] Language badge correct
- [ ] Syntax highlighting works
- [ ] Can write code
- [ ] Run Code button works
- [ ] Shows visible test cases only
- [ ] Submit Solution button works
- [ ] Shows all test cases
- [ ] Can only submit once
- [ ] Hidden cases show "Hidden"

### Timer & Submission
- [ ] Timer counts down
- [ ] Turns red at < 10 min
- [ ] Auto-submits at 0
- [ ] Manual submit works
- [ ] Results page loads

### Results Page
- [ ] Shows total score
- [ ] Shows MCQ breakdown
- [ ] Shows coding breakdown
- [ ] Shows strong/weak topics
- [ ] Shows AI feedback

### Career Intelligence
- [ ] Dashboard loads (after 3 tests)
- [ ] Career DNA shows 5 dimensions
- [ ] Overall score calculated
- [ ] Skill map shows skills
- [ ] Forecasts shown
- [ ] Weekly strategy shown
- [ ] AI insights shown

### Performance Dashboard
- [ ] Key metrics shown
- [ ] Score trend graph works
- [ ] Strong areas shown
- [ ] Weak areas shown
- [ ] AI recommendations shown
- [ ] Daily quote shown

---

## 🎉 COMPLETION CRITERIA

Your testing is **100% COMPLETE** when:

✅ All 21 tests pass  
✅ All checklist items checked  
✅ No critical bugs found  
✅ All features work as described in PHASE6_IMPLEMENTATION_STATUS.md

---

## 📞 SUPPORT

If you encounter issues:

1. Check backend console for errors
2. Check browser console (F12)
3. Check database connection
4. Verify all dependencies installed
5. Review this guide's "Common Issues" section

---

**Happy Testing! 🚀**

Generated: 2026-02-27  
Version: 1.0.0  
Status: Production Ready ✅
