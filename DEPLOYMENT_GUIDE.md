# 🚀 Production Deployment Guide - CareerPilot AI

Complete guide to deploy your full-stack AI application to production using **FREE** services.

---

## 📋 Deployment Stack

| Component | Service | Tier |
|-----------|---------|------|
| **Frontend** | Vercel | Free |
| **Backend** | Render | Free |
| **Database** | Supabase | Free |
| **AI/LLM** | Groq | Free |

---

## 🗂️ Prerequisites

Before deployment, ensure you have:

- ✅ GitHub account with repository: `https://github.com/shahid1330/careerPilot-AI`
- ✅ Vercel account (sign up at https://vercel.com)
- ✅ Render account (sign up at https://render.com)
- ✅ Supabase account (sign up at https://supabase.com)
- ✅ Groq API key (get from https://console.groq.com/keys)

---

## 📊 Environment Variables Summary

### Backend Environment Variables (Render)

```env
DATABASE_URL=postgresql://your-username:your-password@your-host:5432/your-database
JWT_SECRET_KEY=your-super-secret-jwt-key-here-use-openssl-rand-hex-32
LLM_API_KEY=your-groq-api-key-here
LLM_MODEL_NAME=llama-3.1-8b-instant
```

### Frontend Environment Variables (Vercel)

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

---

## 🔧 Part 1: Backend Deployment (Render)

### Step 1: Create New Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"** (or use **"Public Git repository"**)

### Step 2: Configure Repository

**Option A: Connect GitHub (Recommended)**
- Authorize Render to access your GitHub
- Select: `shahid1330/careerPilot-AI`
- Click **"Connect"**

**Option B: Public Git Repository**
- Enter: `https://github.com/shahid1330/careerPilot-AI`
- Click **"Continue"**

### Step 3: Configure Build Settings

Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | `careerpilot-backend` |
| **Region** | Choose closest to you (e.g., Oregon, Frankfurt) |
| **Branch** | `main` |
| **Root Directory** | `backend` ⚠️ IMPORTANT |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install --upgrade pip && pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your Supabase/Railway PostgreSQL URL |
| `JWT_SECRET_KEY` | Your secure JWT secret (use: `openssl rand -hex 32`) |
| `LLM_API_KEY` | Your Groq API key from console.groq.com |
| `LLM_MODEL_NAME` | `llama-3.1-8b-instant` |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Once deployed, you'll get a URL like: `https://careerpilot-backend.onrender.com`

### Step 6: Run Database Migrations

After deployment, go to **"Shell"** tab in Render dashboard and run:

```bash
alembic upgrade head
```

### Step 7: Verify Backend

Test your backend:

```bash
curl https://careerpilot-backend.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**🔗 Save your backend URL - you'll need it for frontend deployment!**

---

## 🎨 Part 2: Frontend Deployment (Vercel)

### Step 1: Import Project

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. If not connected, click **"Continue with GitHub"**
4. Select: `shahid1330/careerPilot-AI`
5. Click **"Import"**

### Step 2: Configure Project

| Field | Value |
|-------|-------|
| **Project Name** | `careerpilot-ai` |
| **Framework Preset** | `Next.js` (auto-detected) |
| **Root Directory** | `frontend` ⚠️ IMPORTANT - Click "Edit" and select `frontend` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `.next` (default) |
| **Install Command** | `npm install` (default) |

### Step 3: Add Environment Variables

Click **"Environment Variables"** section:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | `https://careerpilot-backend.onrender.com` (your backend URL from Step 7 above) |

⚠️ **IMPORTANT**: Replace `careerpilot-backend.onrender.com` with YOUR actual Render backend URL!

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build (3-5 minutes)
3. Once deployed, you'll get a URL like: `https://careerpilot-ai.vercel.app`

### Step 5: Update Backend CORS

After frontend deployment, update your backend on Render:

1. Go to Render dashboard → Your backend service
2. Go to **"Environment"** tab
3. Add a new environment variable:

| Key | Value |
|-----|-------|
| `CORS_ORIGINS` | `https://careerpilot-ai.vercel.app,http://localhost:3000` |

4. Click **"Save Changes"** - this will trigger a redeployment

---

## ✅ Part 3: Post-Deployment Verification

### Test Frontend

1. Visit: `https://careerpilot-ai.vercel.app`
2. Verify landing page loads
3. Click **"Get Started"** or **"Login"**

### Test Registration Flow

1. Go to: `https://careerpilot-ai.vercel.app/register`
2. Create a new account:
   - Email: `test@example.com`
   - Password: `Test123456`
   - Full Name: `Test User`
3. Should successfully create account and redirect to login

### Test Login Flow

1. Go to: `https://careerpilot-ai.vercel.app/login`
2. Login with the account you just created
3. Should redirect to dashboard

### Test AI Features

1. **Career Roadmap Generation**:
   - Go to `/roadmap`
   - Enter role: `Full Stack Developer`
   - Enter timeline: `60 days`
   - Click **"Generate Roadmap"**
   - Should generate AI roadmap

2. **Daily Plan Generation**:
   - Go to `/daily-plan`
   - Select a roadmap
   - Click **"Generate 60-Day Plan"**
   - Should generate daily tasks

3. **Interactive Learning**:
   - Go to `/learn`
   - Enter topic: `React Hooks`
   - Click **"Teach Me"**
   - Should get AI explanation with resources

### Test Profile & Progress

1. Go to `/profile`
2. Verify stats are showing
3. Mark some daily tasks as complete in `/daily-plan`
4. Verify progress updates in dashboard

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: 502 Bad Gateway on Render**
- Solution: Check Render logs, ensure all environment variables are set
- Verify database connection string is correct

**Issue: Database connection failed**
- Solution: Verify DATABASE_URL is correct
- Check Supabase database is running
- Run migrations: `alembic upgrade head`

**Issue: LLM API errors**
- Solution: Verify LLM_API_KEY is correct
- Check Groq API quota/limits

### Frontend Issues

**Issue: API calls failing (CORS errors)**
- Solution: Verify CORS_ORIGINS is set on backend with your Vercel URL
- Check NEXT_PUBLIC_API_URL is correct

**Issue: 404 on routes**
- Solution: This is normal for Next.js on first deploy
- Routes work after first page load

**Issue: Environment variables not working**
- Solution: Ensure variable starts with `NEXT_PUBLIC_`
- Redeploy after adding variables

---

## 📊 Monitoring & Logs

### Backend Logs (Render)

1. Go to Render dashboard
2. Click your service
3. Go to **"Logs"** tab
4. View real-time logs

### Frontend Logs (Vercel)

1. Go to Vercel dashboard
2. Click your project
3. Go to **"Deployments"** → Click latest
4. Click **"Functions"** or **"Runtime Logs"**

---

## 🔄 Redeployment

### Backend (Render)

**Auto-deploy on Git push:**
- Push to `main` branch → Auto-deploys

**Manual deploy:**
- Render dashboard → Click **"Manual Deploy"** → **"Clear build cache & deploy"**

### Frontend (Vercel)

**Auto-deploy on Git push:**
- Push to `main` branch → Auto-deploys

**Manual deploy:**
- Vercel dashboard → Click **"Redeploy"**

---

## 🎯 Final URLs

After successful deployment, you should have:

- **Frontend**: `https://careerpilot-ai.vercel.app`
- **Backend**: `https://careerpilot-backend.onrender.com`
- **API Docs**: `https://careerpilot-backend.onrender.com/docs`

---

## 🔒 Security Checklist

- ✅ All API keys stored as environment variables (not in code)
- ✅ JWT secret is secure and not exposed
- ✅ Database URL uses credentials, not hardcoded
- ✅ CORS configured to only allow your frontend domain
- ✅ .env files in .gitignore (not committed)

---

## 💰 Free Tier Limits

| Service | Limit |
|---------|-------|
| **Render** | 750 hours/month (always on for 1 service) |
| **Vercel** | Unlimited deployments, 100 GB bandwidth |
| **Supabase** | 500 MB database, 1 GB file storage |
| **Groq** | Rate limits apply (check console.groq.com) |

---

## 🎉 Success!

Your full-stack AI Career Roadmap application is now live in production!

**Share your app:**
- Frontend: `https://careerpilot-ai.vercel.app`
- API Docs: `https://careerpilot-backend.onrender.com/docs`

---

## 📞 Support

If you encounter issues:
1. Check Render/Vercel logs
2. Verify all environment variables
3. Test API endpoints with `/docs`
4. Check database connectivity

**Need help?** Open an issue on GitHub: `https://github.com/shahid1330/careerPilot-AI/issues`
