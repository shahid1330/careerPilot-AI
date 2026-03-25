# Test Page Update Requirements

## Issues to Fix:

### 1. Timer Duration ✅ FIXED in mock-test/page.tsx
- 10 MCQ + 2 Coding = 2 hours ✅
- 15 MCQ + 2 Coding = 2.5 hours ✅
- 15 MCQ + 3 Coding = 3 hours ✅
- 10 MCQ + 4 Coding = 3.5 hours ✅
- 20 MCQ + 4 Coding = 3.5 hours ✅

### 2. Network Error ✅ FIXED
- Added better error handling
- Shows clear error messages
- Guides user to check backend

### 3. Remaining Features to Add:

#### A. Reset Code Button
- Add button next to Run/Submit
- Resets code to starter_code
- Confirmation dialog

#### B. Language Selection
- Check roadmap for preferred language
- If language specified → Lock to that language only
- If no language → Show dropdown with all options
- Store in localStorage

#### C. Better Coding Question Format
- Problem description
- Sample input/output
- Explanation
- Constraints
- Clean formatting

## Quick Fix Script Needed

Create a simpler test page that focuses on core functionality while we debug the backend connection.
