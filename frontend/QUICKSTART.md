# 🚀 Quick Start Guide - CareerPilot AI Frontend

## ⚡ 60-Second Setup

### Step 1: Start Backend (if not running)
```bash
cd "E:\Christ University\Trimester 6\Project\backend"
uvicorn main:app --reload
```
✅ Backend: http://localhost:8000

### Step 2: Start Frontend (ALREADY RUNNING)
```bash
cd "E:\Christ University\Trimester 6\Project\frontend"
npm run dev
```
✅ Frontend: http://localhost:3000

---

## 🎯 Test the Application

### 1. Create Account
1. Go to http://localhost:3000
2. Click "Get Started" or "Sign Up"
3. Fill in registration form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `password123`
4. Click "Create Account"
5. ✅ Auto-logged in and redirected to dashboard

### 2. Generate AI Roadmap
1. Click "Create Roadmap" card on dashboard
2. Enter:
   - Target Role: `Full Stack Developer`
   - Duration: `90` days
3. Click "Generate Roadmap"
4. ✅ View AI-generated career roadmap

### 3. Create Daily Plan
1. From roadmap page, click "Generate Daily Plan"
2. Enter User Role ID (from roadmap response)
3. Optionally paste roadmap summary
4. Click "Generate Daily Plan"
5. ✅ See day-by-day learning plan
6. Click any day to mark as complete

### 4. Learn a Topic
1. Go to "Learn" from sidebar
2. Enter topic: `React Hooks`
3. Add context (optional)
4. Click "Learn This Topic"
5. ✅ Get AI explanation with:
   - Detailed explanation
   - Key points
   - Recommended resources
   - Practice suggestions

---

## 📱 Navigation

### Desktop
- **Sidebar**: Left side with icon navigation
- **User Menu**: Top right dropdown

### Mobile
- **Bottom Nav**: 4 main tabs at bottom
- **Burger Menu**: User profile in top right

---

## 🎨 Features to Explore

✅ **Smooth Animations**: Hover over cards and buttons  
✅ **Progress Tracking**: Mark daily tasks complete  
✅ **Responsive Design**: Resize browser window  
✅ **Error Handling**: Try invalid credentials  
✅ **Loading States**: See spinners during API calls  

---

## 🔐 Test Credentials

**Already Created?** Use your credentials  
**New User?** Register a new account (takes 10 seconds)

---

## 🚨 Troubleshooting

### Frontend won't load?
```bash
# Check if dev server is running
# Terminal should show: ✓ Ready in X.Xs
```

### Backend not responding?
```bash
# Start backend:
cd backend
uvicorn main:app --reload
# Check: http://localhost:8000/docs
```

### Can't login?
- Check username (not email) is used for login
- Register a new account if needed

---

## ✅ Success Checklist

- [ ] Landing page loads at http://localhost:3000
- [ ] Can register a new account
- [ ] Auto-redirected to dashboard after signup
- [ ] Dashboard shows welcome card with your name
- [ ] Can generate AI roadmap
- [ ] Can create daily plan
- [ ] Can learn topics with AI
- [ ] Can mark days as complete
- [ ] Can view profile
- [ ] Can logout

---

**Everything Working?** 🎉  
**You're ready to explore CareerPilot AI!**

**Frontend**: http://localhost:3000  
**Backend API**: http://localhost:8000/docs
