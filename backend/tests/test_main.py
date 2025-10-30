# Tests for FastAPI Backend

from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_placeholder():
    assert True

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Agentic RAG Math Agent Backend!"}

def test_query_rag_pipeline():
    with patch("app.main.query_gemini_api") as mock_gemini, \
         patch("app.main.query_perplexity_api") as mock_perplexity:

        mock_gemini.return_value = "Gemini mock response"
        mock_perplexity.return_value = "Perplexity mock response"

        response = client.post("/query", json={"question": "What is 2+2?"})
        assert response.status_code == 200
        assert response.json() == {
            "gemini": "Gemini mock response",
            "perplexity": "Perplexity mock response"
        }