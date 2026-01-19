# 🚀 Phase 3 - Quick Reference

## Installation

```powershell
cd "e:\Christ University\Trimester 6\Project\backend"
.\venv\Scripts\Activate.ps1
pip install httpx==0.26.0
```

## Verify

```powershell
python verify_phase3.py
```

## Run

```powershell
uvicorn main:app --reload
```

## Test

Open: **http://localhost:8000/docs**

---

## API Endpoints (All require JWT token)

### 1. Generate Roadmap
```http
POST /ai/generate-roadmap
Authorization: Bearer <token>

{
  "role_name": "Full Stack Developer",
  "user_role_id": 1
}
```

### 2. Generate Daily Plan
```http
POST /ai/generate-daily-plan
Authorization: Bearer <token>

{
  "role_name": "Python Developer",
  "duration_days": 30,
  "user_role_id": 1
}
```

### 3. Teach Topic
```http
POST /ai/teach-topic
Authorization: Bearer <token>

{
  "topic": "Docker basics"
}
```

---

## Files Added

**AI Module:**
- `app/ai/groq_client.py` - Groq API client
- `app/ai/prompts.py` - Prompt templates

**Services:**
- `app/services/ai_service.py` - Business logic

**Schemas:**
- `app/schemas/ai.py` - Request/Response models

**Routers:**
- `app/routers/ai.py` - 3 AI endpoints

**Docs:**
- `PHASE3_AI_INTEGRATION.md` - Full documentation
- `PHASE3_COMPLETE.md` - Summary
- `verify_phase3.py` - Verification script

---

## Configuration (.env)

```env
LLM_API_KEY=your-groq-api-key-here
LLM_MODEL_NAME=llama-3.1-8b-instant
```

---

## Status: ✅ COMPLETE

All Phase 3 features implemented and tested!
