"""
Minimal FastAPI test to isolate the issue
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/test")
def test():
    return {"status": "working"}

if __name__ == "__main__":
    import uvicorn
    print("Starting minimal test server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
