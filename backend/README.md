# CareerPilot AI - Backend (Phases 2 & 3)

A secure FastAPI backend with PostgreSQL database integration, JWT-based authentication, and AI-powered career guidance features.

## 🚀 Features

### Phase 2: Backend Foundation
- ✅ FastAPI framework with automatic API documentation
- ✅ PostgreSQL database integration using SQLAlchemy ORM
- ✅ JWT-based authentication with OAuth2 password flow
- ✅ Secure password hashing using bcrypt
- ✅ Database migrations with Alembic
- ✅ Modular and scalable project structure
- ✅ Environment-based configuration
- ✅ CORS support for frontend integration

### Phase 3: AI/LLM Integration (NEW!)
- ✅ AI-powered career roadmap generation
- ✅ Personalized daily learning plan creation
- ✅ Interactive topic teaching with AI
- ✅ Groq LLM integration (llama-3.1-8b-instant)
- ✅ Structured JSON responses from AI
- ✅ All AI endpoints JWT-protected

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/                 # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py         # Settings and environment variables
│   │   ├── base.py           # SQLAlchemy base
│   │   └── database.py       # Database connection
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py           # User and UserRole models
│   │   ├── roadmap.py        # Roadmap, DailyPlan, TopicProgress
│   │   ├── test.py           # MockTest, TestResult models
│   │   └── interview.py      # InterviewSession, InterviewFeedback
│   ├── schemas/              # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py           # User schemas
│   │   ├── auth.py           # Authentication schemas
│   │   └── ai.py             # AI request/response schemas (Phase 3)
│   ├── routers/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication routes
│   │   └── ai.py             # AI/LLM routes (Phase 3)
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py       # Password hashing
│   │   └── jwt.py            # JWT token management
│   ├── ai/                   # AI/LLM module (Phase 3)
│   │   ├── __init__.py
│   │   ├── groq_client.py    # Groq API client
│   │   └── prompts.py        # Prompt templates
│   └── services/             # Business logic (Phase 3)
│       ├── __init__.py
│       └── ai_service.py     # AI service layer
├── alembic/                  # Database migrations
│   ├── versions/             # Migration scripts
│   ├── env.py                # Alembic environment
│   └── script.py.mako        # Migration template
├── main.py                   # FastAPI application
├── requirements.txt          # Python dependencies
├── alembic.ini              # Alembic configuration
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment template
├── README.md                # This file
├── PHASE3_AI_INTEGRATION.md # Phase 3 documentation
└── verify_phase3.py         # Phase 3 verification script
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Groq API key (for Phase 3 AI features)

### Step 1: Clone and Navigate

```powershell
cd "e:\Christ University\Trimester 6\Project\backend"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

The `.env` file is already configured with your credentials. Verify it contains:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=careerpilot_ai
DB_USER=postgres
DB_PASSWORD=postgres

JWT_SECRET_KEY=some_random_long_string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DEBUG=False
```

⚠️ **Security Note**: For production, change `JWT_SECRET_KEY` to a strong random string.

### Step 5: Verify Database Connection

Ensure PostgreSQL is running and the database exists:

```powershell
# Test connection (optional)
psql -U postgres -d careerpilot_ai -c "\dt"
```

### Step 6: Run the Application

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## 📡 API Endpoints

### Authentication Endpoints

#### 1. Register User
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepass123",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "created_at": "2026-01-14T10:30:00",
  "updated_at": "2026-01-14T10:30:00"
}
```

#### 2. Login
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepass123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe"
  }
}
```

#### 3. Get Current User (Protected)
```
GET /auth/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "created_at": "2026-01-14T10:30:00",
  "updated_at": "2026-01-14T10:30:00",
  "roles": [
    {
      "id": 1,
      "role_name": "user",
      "granted_at": "2026-01-14T10:30:00"
    }
  ]
}
```

### Root Endpoints

#### Health Check
```
GET /health
```

#### API Root
```
GET /
```

---

## 🤖 Phase 3: AI Endpoints

All AI endpoints require JWT authentication.

### Generate Career Roadmap
```http
POST /ai/generate-roadmap
Authorization: Bearer <access_token>
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

### Generate Daily Learning Plan
```http
POST /ai/generate-daily-plan
Authorization: Bearer <access_token>
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
    }
    // ... more days
  ]
}
```

### AI Topic Teaching
```http
POST /ai/teach-topic
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "topic": "REST API design principles"
}
```

**Response (200 OK):**
```json
{
  "topic": "REST API design principles",
  "explanation": "REST is an architectural style for designing networked applications...",
  "examples": [
    "GET /users - Retrieve list of users",
    "POST /users - Create a new user"
  ],
  "resources": [
    "GeeksforGeeks: REST API Tutorial",
    "W3Schools: REST API",
    "YouTube: REST API Crash Course"
  ]
}
```

**For detailed Phase 3 documentation, see:** [PHASE3_AI_INTEGRATION.md](PHASE3_AI_INTEGRATION.md)

---## 🔒 Authentication Flow

1. **Register**: Create a new user account (`POST /auth/register`)
2. **Login**: Authenticate and receive JWT token (`POST /auth/login`)
3. **Access Protected Routes**: Include token in Authorization header:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

## 🗄️ Database Models

The backend connects to existing PostgreSQL tables:

- **users** - User accounts
- **user_roles** - Role-based access control
- **roadmaps** - Career learning paths
- **daily_plans** - Daily learning tasks
- **topic_progress** - Learning progress tracking
- **mock_tests** - Assessment tests
- **test_results** - Test attempt results
- **interview_sessions** - Mock interview sessions
- **interview_feedback** - Interview feedback data

## 🔧 Database Migrations (Alembic)

### Generate a new migration
```powershell
alembic revision --autogenerate -m "description of changes"
```

### Apply migrations
```powershell
alembic upgrade head
```

### Rollback migration
```powershell
alembic downgrade -1
```

## 🧪 Testing with Swagger UI

1. Start the server: `uvicorn main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Test the endpoints:
   - Try `/auth/register` to create a user
   - Use `/auth/login` to get a token
   - Click "Authorize" button and paste the token
   - Test `/auth/me` to verify authentication

## ⚠️ Error Handling

The API handles common errors:

- **400 Bad Request**: Invalid input (duplicate email/username)
- **401 Unauthorized**: Invalid credentials or missing/invalid token
- **404 Not Found**: Resource not found
- **422 Validation Error**: Request validation failed
- **500 Internal Server Error**: Server error

## 🔐 Security Features

✅ Passwords are hashed using bcrypt (never stored as plain text)  
✅ JWT tokens with expiration (60 minutes by default)  
✅ OAuth2 password flow for authentication  
✅ Environment variables for sensitive data  
✅ CORS middleware for frontend integration  
✅ Input validation using Pydantic  

## 📝 Development Notes

### Adding New Routes
1. Create router in `app/routers/`
2. Define schemas in `app/schemas/`
3. Register router in `main.py`

### Protected Routes
Use the `get_current_user` dependency:

```python
from app.utils.jwt import get_current_user
from app.models.user import User

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

## 🐛 Troubleshooting

### Cannot connect to database
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database `careerpilot_ai` exists

### Import errors
- Activate virtual environment: `.\venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

### Token errors
- Verify `JWT_SECRET_KEY` in `.env`
- Check token hasn't expired
- Ensure token is in format: `Bearer <token>`

## 📚 Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **python-jose** - JWT token handling
- **passlib** - Password hashing
- **uvicorn** - ASGI server

## 🎯 Next Steps (Future Phases)

- [ ] Implement roadmap generation endpoints
- [ ] Add mock test and assessment features
- [ ] Integrate AI for interview preparation
- [ ] Add progress tracking endpoints
- [ ] Implement file upload for resumes
- [ ] Add email verification
- [ ] Rate limiting and API throttling

## 📄 License

This project is part of the Christ University Trimester 6 project.

---

**Created by**: Senior Backend Engineer  
**Phase**: 2 - Backend Foundation & Authentication  
**Date**: January 14, 2026
