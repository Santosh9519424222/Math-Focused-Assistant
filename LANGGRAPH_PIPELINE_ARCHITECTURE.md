# LangGraph Pipeline Architecture

## Overview

The LangGraph pipeline orchestrates the Agentic RAG workflow for math problem solving. It manages state transitions, routing logic, and integration with the knowledge base, Gemini API, and web search fallback.

## Diagram

```
User Question
     ↓
┌─────────────────────────────────────────────┐
│         FastAPI Backend (Port 8000)         │
│  ┌───────────────────────────────────────┐  │
│  │      LangGraph Workflow (Agentic)     │  │
│  │ ┌───────────────────────────────────┐ │  │
│  │ │ 1. Search Database (Qdrant)       │ │  │
│  │ └─────────────┬─────────────────────┘ │  │
│  │               ↓                       │  │
│  │   Found? ──┬──Yes──→ Gemini           │  │
│  │            │                          │  │
│  │            └──No──→ Web Search        │  │
│  │                      ↓                │  │
│  │             Found? ──┬──Yes           │  │
│  │                      │                │  │
│  │                      └──No            │  │
│  │                          ↓            │  │
│  │                     Not Found         │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
     ↓
React Frontend (Port 3000)
```

## State Machine Steps

1. **Input Guardrails**: Validate user question for math relevance and safety.
2. **Vector Search**: Query Qdrant for similar problems using sentence-transformers.
3. **Routing Logic**: If confidence ≥ 50%, use KB answer (Gemini); else, fallback to web search (Perplexity).
4. **Answer Generation**: Retrieve solution from KB or generate via Gemini/web search.
5. **Output Guardrails**: Validate and sanitize response.
6. **HITL Feedback**: Collect user ratings and corrections for continuous improvement.

## Integration Points
- **Qdrant**: Vector database for semantic search.
- **Gemini API**: AI-powered math solutions.
- **Perplexity API**: Web search fallback.
- **DSPy**: Feedback pattern analysis and recommendations.
- **MCP Server**: External agent integration.

## Extensibility
- Add new states for additional validation, fallback, or enrichment.
- Integrate more APIs or KB sources as needed.
- Use DSPy to optimize routing and learning.

## References
- See `backend/app/langgraph_workflow.py` for implementation details.
- See `README.md` for full system architecture.
