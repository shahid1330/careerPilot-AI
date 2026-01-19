# 🚀 CareerPilot AI

> **AI-Powered Career Roadmap & Learning Platform**  
> Transform your career goals into actionable daily plans with intelligent AI guidance.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

---

## 📖 Overview

**CareerPilot AI** is a full-stack AI-powered platform that helps users plan their career journey by generating personalized learning roadmaps, daily action plans, and interactive learning resources. Built with modern technologies and powered by Groq's LLM, it provides intelligent career guidance tailored to individual goals.

### 🎯 Key Features

- **🗺️ AI-Generated Career Roadmaps** - Get personalized career paths based on your target role and timeline
- **📅 Daily Learning Plans** - Break down your roadmap into 60 days of actionable tasks
- **📚 Interactive Learning** - AI-powered topic explanations with curated resources
- **📊 Progress Tracking** - Monitor your learning journey with detailed statistics and streaks
- **👤 User Profiles** - Manage your account and track your achievements
- **🔐 Secure Authentication** - JWT-based authentication with secure session management
- **⚡ Real-time AI** - Powered by Groq's lightning-fast LLM inference

---

## 🛠️ Tech Stack

### **Backend**
- **FastAPI** - Modern, high-performance Python web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration management
- **JWT** - Secure token-based authentication
- **Groq LLM** - AI-powered content generation
- **Passlib** - Password hashing and security
- **Python-Jose** - JWT token handling

### **Frontend**
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS v4** - Utility-first styling
- **Shadcn/UI** - Beautiful, accessible UI components
- **Framer Motion** - Smooth animations and transitions
- **Lucide Icons** - Modern icon library
- **Axios** - HTTP client for API calls

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** (for backend)
- **Node.js 18+** (for frontend)
- **PostgreSQL 12+** (database)
- **Git** (version control)

### Environment Variables

You'll need to create `.env` files for both backend and frontend:

#### Backend `.env` (root: `backend/.env`)
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/careerpilot

# JWT
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq AI
GROQ_API_KEY=your-groq-api-key-here

# CORS
CORS_ORIGINS=http://localhost:3000
```

#### Frontend `.env.local` (root: `frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> **Note:** See `.env.example` files in both directories for reference.

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/shahid1330/careerPilot-AI.git
cd careerPilot-AI
```

### 2️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file (see Backend .env section above)

# Run database migrations
alembic upgrade head

# Start the FastAPI server
uvicorn main:app --reload
```

### 3️⃣ Frontend Setup

Open a **new terminal** and:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Set up environment variables
# Create .env.local file (see Frontend .env.local section above)

# Start the Next.js development server
npm run dev
# or
yarn dev
```

---

## 📂 Project Structure

```
careerPilot-AI/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── ai/               # AI service & prompts
│   │   ├── api/              # API routes
│   │   ├── core/             # Core configs (security, database)
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic
│   ├── main.py               # FastAPI application entry
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variables template
│
├── frontend/
│   ├── app/                  # Next.js App Router pages
│   │   ├── dashboard/        # Dashboard page
│   │   ├── roadmap/          # Career roadmap generator
│   │   ├── daily-plan/       # Daily learning plans
│   │   ├── learn/            # Interactive learning
│   │   ├── profile/          # User profile
│   │   ├── login/            # Authentication
│   │   └── register/         # User registration
│   ├── components/           # React components
│   │   └── ui/               # Shadcn UI components
│   ├── context/              # React Context (Auth)
│   ├── lib/                  # Utilities & services
│   ├── public/               # Static assets
│   ├── package.json          # Node dependencies
│   └── .env.local.example    # Environment variables template
│
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

---

## 🎮 Usage

1. **Register** - Create a new account at `/register`
2. **Login** - Sign in at `/login`
3. **Create Roadmap** - Go to `/roadmap` and enter your target role and timeline
4. **Generate Daily Plan** - Navigate to `/daily-plan` to generate your 60-day learning plan
5. **Track Progress** - Mark days as completed and track your streak
6. **Learn Topics** - Use `/learn` for AI-powered topic explanations
7. **View Profile** - Check your stats and achievements at `/profile`

---

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login (returns JWT)

### Roadmaps
- `POST /api/roadmaps/generate` - Generate AI career roadmap
- `GET /api/roadmaps/` - Get user's roadmaps

### Daily Plans
- `POST /api/daily-plans/generate` - Generate 60-day plan
- `GET /api/daily-plans/` - Get user's daily plans

### Learning
- `POST /api/ai/teach` - Get AI explanation for a topic

---

## 🌟 Features in Detail

### AI Career Roadmaps
- Personalized based on target role (e.g., "Full Stack Developer")
- Customizable timeline (30, 60, 90 days)
- Comprehensive learning path with milestones
- Technologies and skills breakdown

### Daily Learning Plans
- 60-day structured curriculum
- Daily tasks with clear objectives
- Progress tracking with completion checkmarks
- Expandable daily details

### Interactive Learning
- AI-powered topic explanations
- Key points extraction
- Curated YouTube tutorials (Code with Harry)
- External learning resources
- Prerequisite topics

### Progress Dashboard
- Total roadmaps created
- Days completed statistics
- Learning streak tracking
- Today's pending tasks
- Motivational achievements

---

## 🔒 Security

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - Bcrypt for password security
- **CORS Protection** - Configured for frontend origin
- **Environment Variables** - Sensitive data stored in .env files
- **SQL Injection Prevention** - SQLAlchemy ORM parameterized queries

---

## 🚢 Deployment

### Backend Deployment (Render/Railway/Heroku)

1. Set environment variables on your platform
2. Update `DATABASE_URL` to production PostgreSQL
3. Run migrations: `alembic upgrade head`
4. Deploy with: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel/Netlify)

1. Connect your GitHub repository
2. Set `NEXT_PUBLIC_API_URL` to your backend URL
3. Build command: `npm run build`
4. Deploy automatically on push

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

---

## 👨‍💻 Author

**Mohammad Shahid Raza**  
GitHub: [@shahid1330](https://github.com/shahid1330)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing Python web framework
- [Next.js](https://nextjs.org/) - The React framework for production
- [Groq](https://groq.com/) - Lightning-fast AI inference
- [Shadcn/UI](https://ui.shadcn.com/) - Beautiful component library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

## 📧 Support

For questions or support, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please give it a star!**
