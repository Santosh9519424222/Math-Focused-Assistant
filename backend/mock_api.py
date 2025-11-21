"""
Minimal FastAPI Backend Mock for Testing Frontend
This runs without heavy dependencies like dspy, langchain, etc.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(title="Math Agent Mock API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    difficulty: Optional[str] = "JEE_Main"
    topic: Optional[str] = None

@app.get("/")
def root():
    return {
        "message": "Math Agent Mock API - Frontend Testing",
        "status": "online",
        "version": "1.0.0-mock",
        "endpoints": ["/query", "/feedback", "/problem_status"]
    }

@app.post("/query")
def query_endpoint(query: Query):
    """Mock query endpoint for testing frontend"""
    return {
        "question": query.question,
        "answer": f"Mock Solution for: {query.question}\n\nStep 1: Analyze the problem\nStep 2: Apply relevant formula\nStep 3: Calculate the result\n\nThis is a test response. Deploy the full backend for real solutions.",
        "difficulty": query.difficulty,
        "confidence": 0.95,
        "sources": ["Mock Source 1", "Mock Source 2"],
        "feedback_submitted": False
    }

@app.post("/feedback")
def feedback_endpoint(feedback: dict):
    """Mock feedback endpoint"""
    return {
        "status": "success",
        "message": "Feedback received (mock)",
        "feedback_id": "mock-123"
    }

@app.get("/problem_status")
def problem_status():
    """Mock problem status endpoint"""
    return {
        "total_problems": 42,
        "solved_problems": 38,
        "solve_rate": 90.5,
        "by_type": {
            "solved": 38,
            "unsolved": 4
        }
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "mode": "mock"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

