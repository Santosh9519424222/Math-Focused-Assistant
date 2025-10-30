# Agentic RAG Math Agent

An intelligent math problem-solving system with **Agentic RAG architecture**, **LangGraph workflow orchestration**, and **Model Context Protocol (MCP) server** integration.

## 🎯 Features

- ✅ **Agentic RAG Architecture** with LangGraph state machine
- ✅ **Vector Knowledge Base** (Qdrant + sentence-transformers)
- ✅ **Semantic Search** for similar problem matching
- ✅ **AI-Powered Solutions** (Gemini API)
- ✅ **Web Search Fallback** (Perplexity API)
- ✅ **MCP Server** for AI agent integration ⭐ NEW!
- ✅ **OCR Support** (upload images or paste screenshots)
- ✅ **Math Keyboard** (70+ symbols in 9 categories)
- ✅ **Modern React UI** with confidence badges

## 📋 Architecture

```
User Question
     ↓
┌────────────────────────────────────────┐
│      FastAPI Backend (Port 8000)       │
│  ┌──────────────────────────────────┐  │
│  │   LangGraph Workflow (Agentic)   │  │
│  │  ┌──────────────────────────┐    │  │
│  │  │ 1. Search Database       │    │  │
│  │  └──────────┬───────────────┘    │  │
│  │             ↓                     │  │
│  │    Found? ──┬── Yes → Gemini     │  │
│  │             │                     │  │
│  │             └── No → Web Search   │  │
│  │                      ↓            │  │
│  │             Found? ──┬── Yes     │  │
│  │                      │            │  │
│  │                      └── No       │  │
│  │                           ↓       │  │
│  │                      Not Found    │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
     ↓
React Frontend (Port 3000)
```

## 🚀 Quick Start

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   .\.venv\Scripts\Activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (`.env` file):
   ```
   GEMINI_API_KEY=your_gemini_key
   PERPLEXITY_API_KEY=your_perplexity_key
   ```

5. Start the FastAPI server:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```
   Server runs on: http://localhost:8000

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   App runs on: http://localhost:3000

### MCP Server (Optional)
To connect with Claude Desktop or other MCP clients:

1. Run the MCP server:
   ```bash
   cd backend
   python mcp_server.py
   ```

2. Configure Claude Desktop (see `backend/MCP_README.md` for details)

3. Available MCP tools:
   - `search_math_problems` - Search knowledge base
   - `get_problem_details` - Get full solutions
   - `list_topics` - List available topics

## 🧪 Running Tests

1. Set the `PYTHONPATH` environment variable:
   ```bash
   $env:PYTHONPATH="backend"  # Windows
   export PYTHONPATH="backend"  # macOS/Linux
   ```

2. Run the tests:
   ```bash
   python -m pytest backend/tests
   ```

3. Or run specific test file:
   ```bash
   python backend/scripts/test_api.py
   ```

## 📚 Project Structure

```
new chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app with LangGraph
│   │   ├── langgraph_workflow.py   # LangGraph state machine
│   │   └── vector_db.py            # Qdrant knowledge base
│   ├── scripts/
│   │   ├── populate_kb.py          # Populate knowledge base
│   │   └── test_api.py             # API testing
│   ├── mcp_server.py               # MCP server for AI agents
│   ├── MCP_README.md               # MCP documentation
│   ├── requirements.txt            # Python dependencies
│   └── .env                        # API keys
├── frontend/
│   ├── src/
│   │   ├── App.js                  # Main React component
│   │   └── App.css                 # Styling
│   ├── package.json                # Node dependencies
│   └── public/
└── README.md                       # This file
```

## 🔧 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - Workflow orchestration
- **Qdrant** - Vector database (in-memory)
- **sentence-transformers** - Local embeddings (all-MiniLM-L6-v2)
- **Gemini API** - AI-powered solutions
- **Perplexity API** - Web search
- **MCP SDK** - Model Context Protocol server

### Frontend
- **React 18** - UI framework
- **Tesseract.js** - OCR for image scanning
- **CSS3** - Modern styling with animations

## 📝 Usage Examples

### Web Interface
1. **Type a question** or paste an image (Ctrl+V)
2. **Select difficulty** (JEE Main or JEE Advanced)
3. **Click "Get Answer"**
4. View step-by-step solution with confidence scores

### API Endpoint
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Solve x³ - 3x + 2 = 0",
    "difficulty": "JEE_Main"
  }'
```

### MCP Tools (via Claude Desktop)
```
Use search_math_problems to find integration problems
Get details for calc_001
List all available topics
```

## 🎓 Knowledge Base

Currently contains 5 JEE-level problems:
- **calc_001**: Integration by parts
- **alg_001**: Cubic equations
- **calc_004**: Logarithmic differentiation
- **prob_001**: Probability combinations
- **trig_001**: Maclaurin series

## 🔮 Future Enhancements

- [ ] Input/Output Guardrails (AI Gateway)
- [ ] Human-in-the-Loop Feedback with DSPy
- [ ] Expand Knowledge Base to 50+ problems
- [ ] JEEBench Benchmarking
- [ ] Final Proposal PDF
- [ ] Demo Video

## 📖 Documentation

- **MCP Server Guide**: `backend/MCP_README.md`
- **API Documentation**: http://localhost:8000/docs (when server running)
- **LangGraph Workflow**: See `backend/app/langgraph_workflow.py`

## 🤝 Contributing

This is a learning project for understanding Agentic RAG systems. Feel free to explore and extend!

## 📄 License

Educational Project - Feel free to use and modify