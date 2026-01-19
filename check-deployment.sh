#!/bin/bash

# ==========================================
# CareerPilot AI - Quick Deployment Check
# ==========================================
# This script helps verify your deployment configuration

echo "🚀 CareerPilot AI - Deployment Configuration Check"
echo "=================================================="
echo ""

# Check if we're in the project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "✅ Project structure verified"
echo ""

# Check backend files
echo "📦 Checking backend deployment files..."
if [ -f "backend/requirements.txt" ]; then
    echo "  ✅ requirements.txt found"
else
    echo "  ❌ requirements.txt missing"
fi

if [ -f "backend/main.py" ]; then
    echo "  ✅ main.py found"
else
    echo "  ❌ main.py missing"
fi

if [ -f "backend/Procfile" ]; then
    echo "  ✅ Procfile found"
else
    echo "  ❌ Procfile missing"
fi

if [ -f "backend/runtime.txt" ]; then
    echo "  ✅ runtime.txt found"
else
    echo "  ❌ runtime.txt missing"
fi

echo ""

# Check frontend files
echo "🎨 Checking frontend deployment files..."
if [ -f "frontend/package.json" ]; then
    echo "  ✅ package.json found"
else
    echo "  ❌ package.json missing"
fi

if [ -f "frontend/next.config.ts" ]; then
    echo "  ✅ next.config.ts found"
else
    echo "  ❌ next.config.ts missing"
fi

if [ -f "frontend/vercel.json" ]; then
    echo "  ✅ vercel.json found"
else
    echo "  ❌ vercel.json missing"
fi

echo ""

# Environment variables check
echo "🔐 Environment Variables Required:"
echo ""
echo "Backend (Render):"
echo "  - DATABASE_URL"
echo "  - JWT_SECRET_KEY"
echo "  - LLM_API_KEY"
echo "  - LLM_MODEL_NAME"
echo ""
echo "Frontend (Vercel):"
echo "  - NEXT_PUBLIC_API_URL"
echo ""

echo "=================================================="
echo "✅ Pre-deployment check complete!"
echo ""
echo "📖 Next steps:"
echo "1. Read DEPLOYMENT_GUIDE.md for detailed instructions"
echo "2. Deploy backend to Render (backend folder only)"
echo "3. Deploy frontend to Vercel (frontend folder only)"
echo "4. Configure environment variables on both platforms"
echo ""
echo "🔗 Repository: https://github.com/shahid1330/careerPilot-AI"
echo "=================================================="
