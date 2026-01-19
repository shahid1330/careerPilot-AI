# CareerPilot AI - Frontend

## 🚀 Phase 4: Production-Ready Frontend

A modern, Big Tech-level frontend built with Next.js, TypeScript, Tailwind CSS, and Shadcn/UI.

---

## ✨ Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Components**: Shadcn/UI
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **State Management**: React Context API

---

## 📁 Project Structure

```
frontend/
├── app/
│   ├── (public)
│   │   ├── page.tsx              # Landing page
│   │   ├── login/page.tsx        # Login page
│   │   └── register/page.tsx     # Register page
│   ├── dashboard/
│   │   ├── layout.tsx            # Dashboard layout with sidebar
│   │   └── page.tsx              # Dashboard home
│   ├── roadmap/
│   │   ├── layout.tsx
│   │   └── page.tsx              # AI Roadmap generation
│   ├── daily-plan/
│   │   ├── layout.tsx
│   │   └── page.tsx              # Daily learning plans
│   ├── learn/
│   │   ├── layout.tsx
│   │   └── page.tsx              # AI topic teaching
│   ├── profile/
│   │   ├── layout.tsx
│   │   └── page.tsx              # User profile
│   ├── layout.tsx                # Root layout with AuthProvider
│   └── globals.css               # Global styles
├── components/
│   └── ui/                       # Shadcn/UI components
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── form.tsx
│       └── ...15 components total
├── context/
│   └── AuthContext.tsx           # Authentication context
├── lib/
│   ├── api.ts                    # Axios instance with interceptors
│   ├── auth.ts                   # Auth service functions
│   ├── ai-service.ts             # AI/LLM service functions
│   └── utils.ts                  # Utility functions
├── middleware.ts                 # Route protection
└── .env.local                    # Environment variables
```

---

## 🚦 Getting Started

### Prerequisites
- Node.js 18+ installed
- Backend running on `http://localhost:8000`

### Start Development Server

```bash
cd "E:\Christ University\Trimester 6\Project\frontend"
npm run dev
```

The app will run on **http://localhost:3000**

---

## 🌐 Environment Variables

`.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## 📱 Pages Overview

- **Landing** (`/`): Hero, features, CTA
- **Login** (`/login`): Authentication
- **Register** (`/register`): Account creation
- **Dashboard** (`/dashboard`): Overview & quick actions
- **Roadmap** (`/roadmap`): AI roadmap generation
- **Daily Plan** (`/daily-plan`): Day-by-day plans
- **Learn** (`/learn`): AI topic teaching
- **Profile** (`/profile`): User account

---

## 🤖 AI Integration

All AI endpoints connected to FastAPI backend:
- **POST /ai/generate-roadmap**: Create career roadmap
- **POST /ai/generate-daily-plan**: Generate daily tasks
- **POST /ai/teach-topic**: Get topic explanations

---

## ✅ Features Complete

- ✅ JWT authentication with auto-logout
- ✅ Protected routes with AuthContext
- ✅ Shadcn/UI components (15+ components)
- ✅ Framer Motion animations
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Error handling & loading states
- ✅ Big Tech-level UI polish
- ✅ Production-ready architecture

---

**Built with ❤️ for CareerPilot AI**
