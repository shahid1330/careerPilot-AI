# Phase 3: AI/LLM Integration - COMPLETE ✅

## 🎯 Overview

Phase 3 adds AI-powered features to CareerPilot using Groq's LLM (llama-3.1-8b-instant). This enables intelligent career roadmap generation, personalized daily learning plans, and interactive topic teaching.

---

## 🚀 New Features Implemented

### 1️⃣ Career Roadmap Generation
**Endpoint**: `POST /ai/generate-roadmap`

- Input: Job role/career path
- AI generates comprehensive roadmap with:
  - Required skills
  - Phased learning path (Fundamentals → Intermediate → Advanced)
  - Recommended projects
- Stores result in `roadmaps` table

### 2️⃣ Daily Learning Plan Generation
**Endpoint**: `POST /ai/generate-daily-plan`

- Input: Role name + duration (1-365 days)
- AI generates day-by-day study plan with:
  - Daily topics building progressively
  - Estimated hours per day (2-6 hours)
  - Coverage from basics to advanced
- Stores results in `daily_plans` table

### 3️⃣ AI Topic Teaching
**Endpoint**: `POST /ai/teach-topic`

- Input: Any topic name
- AI provides:
  - Clear, beginner-friendly explanation
  - Practical examples with code/scenarios
  - Learning resources (GeeksforGeeks, W3Schools, YouTube, Docs)
- Returns response directly (NOT stored in DB)

---

## 📁 New Files Created

### AI Module (`app/ai/`)
```
app/ai/
├── __init__.py
├── groq_client.py      # Groq API client with JSON parsing
└── prompts.py          # Structured prompt templates
```

### Services (`app/services/`)
```
app/services/
├── __init__.py
└── ai_service.py       # Business logic for AI features
```

### Schemas (`app/schemas/`)
```
app/schemas/
└── ai.py              # Pydantic models for AI requests/responses
```

### Routers (`app/routers/`)
```
app/routers/
└── ai.py              # AI endpoints (JWT-protected)
```

---

## 🔧 Files Modified

1. **`app/core/config.py`** - Added LLM configuration
2. **`.env`** - Added LLM_API_KEY and LLM_MODEL_NAME
3. **`main.py`** - Registered AI router
4. **`requirements.txt`** - Added httpx for API calls

---

## ⚙️ Configuration

### Environment Variables
```env
# LLM Configuration (Phase 3)
LLM_API_KEY=your-groq-api-key-here
LLM_MODEL_NAME=llama-3.1-8b-instant
```

### Settings (`app/core/config.py`)
```python
LLM_API_KEY: str
LLM_MODEL_NAME: str = "llama-3.1-8b-instant"
LLM_TIMEOUT: int = 30  # seconds
LLM_MAX_TOKENS: int = 2048
```

---

## 🧪 API Testing Guide

### Prerequisites
1. Install new dependency: `pip install httpx==0.26.0`
2. Ensure LLM_API_KEY is set in `.env`
3. Have a valid JWT token from `/auth/login`

---

### 1. Generate Career Roadmap

**Request:**
```http
POST /ai/generate-roadmap
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "role_name": "Full Stack Developer",
  "user_role_id": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_role_id": 1,
  "roadmap_text": "{\"role\":\"Full Stack Developer\",\"required_skills\":[...],\"learning_path\":[...]}",
  "generated_at": "2026-01-15T10:30:00"
}
```

**What happens:**
- AI generates structured roadmap
- Stored in `roadmaps` table as JSON text
- Associated with user_role_id

---

### 2. Generate Daily Learning Plan

**Request:**
```http
POST /ai/generate-daily-plan
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "role_name": "Python Backend Developer",
  "duration_days": 30,
  "user_role_id": 1
}
```

**Response (201 Created):**
```json
{
  "message": "Successfully generated 30-day learning plan",
  "total_days": 30,
  "plans": [
    {
      "id": 1,
      "user_role_id": 1,
      "day_number": 1,
      "topic": "Introduction to Python Backend Development",
      "estimated_hours": 3
    },
    {
      "id": 2,
      "user_role_id": 1,
      "day_number": 2,
      "topic": "Python Fundamentals - Variables and Data Types",
      "estimated_hours": 4
    }
    // ... 28 more days
  ]
}
```

**What happens:**
- AI generates day-by-day plan
- Each day stored in `daily_plans` table
- Topics build progressively

---

### 3. AI Topic Teaching

**Request:**
```http
POST /ai/teach-topic
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "topic": "REST API design principles"
}
```

**Response (200 OK):**
```json
{
  "topic": "REST API design principles",
  "explanation": "REST (Representational State Transfer) is an architectural style for designing networked applications. It uses HTTP methods to perform CRUD operations...",
  "examples": [
    "GET /users - Retrieve list of users",
    "POST /users - Create a new user",
    "PUT /users/1 - Update user with ID 1"
  ],
  "resources": [
    "GeeksforGeeks: REST API Tutorial",
    "W3Schools: REST API Introduction",
    "YouTube: REST API Crash Course",
    "Documentation: MDN Web Docs - HTTP"
  ]
}
```

**What happens:**
- AI generates educational content
- Returned directly to client
- NOT stored in database

---

## 🔒 Security

- ✅ All AI endpoints require JWT authentication
- ✅ LLM API key stored in environment variables
- ✅ User role validation before DB operations
- ✅ Timeout protection (30 seconds)
- ✅ Error handling for LLM failures

---

## 🏗️ Architecture

```
Client Request
     ↓
JWT Authentication (get_current_user)
     ↓
AI Router (/ai/*)
     ↓
AI Service (Business Logic)
     ↓
Groq Client (LLM API)
     ↓
Prompt Templates (Structured Prompts)
     ↓
Parse JSON Response
     ↓
Store in Database (roadmaps/daily_plans)
     ↓
Return Response to Client
```

---

## 🛠️ How It Works

### Groq Client (`app/ai/groq_client.py`)
- Sends requests to Groq API
- Handles JSON parsing from LLM responses
- Strips markdown code blocks if present
- 30-second timeout protection

### Prompt Templates (`app/ai/prompts.py`)
- Structured prompts for consistent LLM output
- Forces JSON responses
- Clear instructions for format

### AI Service (`app/services/ai_service.py`)
- Validates user_role_id exists
- Calls Groq client with appropriate prompt
- Parses and validates LLM response
- Creates database records
- Returns formatted results

---

## 📊 Database Integration

### Tables Used (Read-Only Schema)

**roadmaps**
```sql
- id (SERIAL, PRIMARY KEY)
- user_role_id (INT, FK → user_roles.id)
- roadmap_text (TEXT, NOT NULL)
- generated_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

**daily_plans**
```sql
- id (SERIAL, PRIMARY KEY)
- user_role_id (INT, FK → user_roles.id)
- day_number (INT, NOT NULL)
- topic (TEXT, NOT NULL)
- estimated_hours (INT, NOT NULL)
```

---

## ⚠️ Error Handling

### Common Errors

**1. LLM API Timeout**
```json
{
  "detail": "Failed to generate roadmap: LLM request timed out after 30 seconds"
}
```

**2. Invalid User Role**
```json
{
  "detail": "UserRole with id 999 not found"
}
```

**3. JSON Parsing Error**
```json
{
  "detail": "Failed to generate roadmap: Failed to parse LLM response as JSON"
}
```

**4. Missing API Key**
```
ValueError: LLM_API_KEY not configured in environment variables
```

---

## 🧩 Integration with Phase 2

Phase 3 extends Phase 2 WITHOUT breaking changes:

- ✅ Uses existing authentication (JWT)
- ✅ Uses existing database tables
- ✅ Uses existing User and UserRole models
- ✅ Adds new `/ai/*` endpoints
- ✅ Phase 2 endpoints continue to work

---

## 🚀 Installation & Running

### 1. Install New Dependencies
```powershell
cd "e:\Christ University\Trimester 6\Project\backend"
.\venv\Scripts\Activate.ps1
pip install httpx==0.26.0
```

### 2. Verify Configuration
Check `.env` file has:
```env
LLM_API_KEY=your-groq-api-key-here
LLM_MODEL_NAME=llama3-8b-8192
```

### 3. Start Server
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test in Swagger
Open: http://localhost:8000/docs

You'll see new section: **AI & LLM** with 3 endpoints

---

## 📝 Testing Workflow

1. **Register/Login** (Phase 2)
   ```
   POST /auth/register
   POST /auth/login
   ```

2. **Get JWT Token**
   - Copy access_token from login response

3. **Authorize in Swagger**
   - Click "Authorize" button
   - Paste token
   - Click "Authorize"

4. **Test AI Endpoints**
   - POST /ai/generate-roadmap
   - POST /ai/generate-daily-plan
   - POST /ai/teach-topic

---

## 🎯 What Works Now

✅ JWT-protected AI endpoints  
✅ Groq LLM integration  
✅ Structured JSON responses from LLM  
✅ Database storage (roadmaps, daily_plans)  
✅ Error handling for LLM failures  
✅ Timeout protection  
✅ User role validation  
✅ Swagger documentation  
✅ Phase 2 compatibility  

---

## 📚 Example Use Cases

### Use Case 1: Career Switch
User wants to become a "Data Scientist"
1. Call `/ai/generate-roadmap` → Get skills & learning path
2. Call `/ai/generate-daily-plan` (90 days) → Get structured plan
3. Call `/ai/teach-topic` ("Machine Learning basics") → Learn concepts

### Use Case 2: Quick Learning
User wants to learn "Docker"
1. Call `/ai/teach-topic` → Get explanation, examples, resources

### Use Case 3: Bootcamp Preparation
User preparing for "Frontend Developer" role
1. Generate roadmap
2. Generate 60-day plan
3. Use teach-topic for unclear concepts

---

## 🔮 Future Enhancements (Not in Phase 3)

- ❌ Mock tests (Future phase)
- ❌ Interview preparation (Future phase)
- ❌ Voice AI (Future phase)
- ❌ Progress tracking (Future phase)

---

## 🐛 Troubleshooting

### Issue: "LLM_API_KEY not configured"
**Solution**: Add to `.env`:
```env
LLM_API_KEY=your-groq-api-key-here
```

### Issue: "module 'app.routers' has no attribute 'ai'"
**Solution**: Ensure `app/routers/ai.py` exists and main.py imports it

### Issue: LLM timeout
**Solution**: Increase timeout in config.py or reduce complexity of prompt

### Issue: JSON parsing error
**Solution**: LLM returned invalid JSON - retry the request

---

## 📞 Support

All Phase 3 features are production-ready and tested. If issues arise:
1. Check `.env` has LLM_API_KEY
2. Verify httpx is installed
3. Check Swagger UI for endpoint details
4. Review error messages for specific issues

---

**Status**: ✅ **PHASE 3 COMPLETE**  
**Last Updated**: January 15, 2026  
**Phase**: 3 - AI/LLM Integration  
