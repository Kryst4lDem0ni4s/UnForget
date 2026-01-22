"""
Minimal test server to diagnose the hanging issue
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Minimal server works"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_minimal:app", host="127.0.0.1", port=8001, reload=False)
