# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'e:\Christ University\Trimester 6\Project\backend'; python -m uvicorn main:app --host 127.0.0.1 --port 8000"

# Wait 3 seconds
Start-Sleep -Seconds 3

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'e:\Christ University\Trimester 6\Project\frontend'; npm run dev"

Write-Host "✅ Both servers starting in separate windows..."
Write-Host "Backend: http://127.0.0.1:8000"
Write-Host "Frontend: http://localhost:3000"
