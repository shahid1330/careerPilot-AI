@echo off
cd /d "e:\Christ University\Trimester 6\Project\backend"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
