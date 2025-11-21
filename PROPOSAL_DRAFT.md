# Final Proposal Draft - Agentic RAG Math Routing Agent

## 1. Overview
This system implements an Agentic-RAG Math Assistant that emulates a mathematics professor: retrieving known problems, generating step-by-step solutions, performing web search when needed, enforcing guardrails, and learning from human feedback.

## 2. Architecture Summary
- FastAPI backend exposing query, guardrail validation, and feedback endpoints.
- LangGraph workflow orchestrating retrieval + decision + generation:
  1. `search_database` (Qdrant vector similarity)
  2. Decision: `kb_internal` (medium/high confidence) OR `perplexity_analyze` (low/none)
  3. `perplexity_analyze` (web search + reasoning via Perplexity)
  4. Decision: success or `not_found`
- Guardrails (InputGuardrails + OutputGuardrails) wrap both ends.
- Feedback loop (HITLFeedbackSystem + DSPyOptimizer) collects ratings/corrections and suggests improvements.
- MCP Server exposes KB tools (`search_math_problems`, `get_problem_details`, `list_topics`).

## 3. Input & Output Guardrails
### Approach
Implemented deterministic rule-based validation:
- Input: Keyword/symbol detection, prohibited term filtering, math relevance score; rejects non-math or harmful queries.
- Output: Harmful content regex filters, low-quality heuristics, math relevance check, sanitization (URLs, emails, phones).
### Rationale
Fast, transparent, easy to audit, lowers risk of unsafe or off-topic content without relying on opaque external moderation models.

## 4. Knowledge Base
### Dataset
Currently a seed set of 5 curated problems (Calculus, Algebra, Probability, Trigonometry). Vectorized via `sentence-transformers` (`all-MiniLM-L6-v2`) into an in-memory Qdrant collection.
### Planned Expansion
- Ingest larger JEE-style dataset (at least 200 problems)
- Add admin ingestion & correction promotion
- Persist Qdrant data beyond process lifecycle
### Example KB Queries
1. "Evaluate ∫₀¹ x² ln(x) dx" → Internal KB answer
2. "Find derivative of x^x" → Internal KB answer (structured steps)

## 5. Web Search / MCP Strategy
- Current: Perplexity API used for blended search + answer generation.
- MCP: Server provides KB tools; integration into workflow planned (tool invocation for retrieval augmentation).
- Planned: Add dedicated web search API (Tavily) → retrieve JSON → summarizer step with guardrails post-process.
### Example Non-KB Queries
1. "Explain Cauchy-Schwarz inequality" → Perplexity web answer
2. "Applications of Maclaurin series in physics" → Perplexity web answer

## 6. Human-in-the-Loop Routing & Learning
### Feedback Flow
User → `/feedback/submit` → Stored in JSON → DSPyOptimizer analyzes negative feedback → suggestions & topic coverage.
### Learning Strategy
- Phase 1 (now): Analytics & suggestions
- Phase 2: Auto-curate corrections → candidate KB entries
- Phase 3: DSPy prompt optimization cycle (generate refined exemplars for weak topics)

## 7. Benchmark Plan (JEE Bench) [Planned]
### Methodology
- Map each JEE Bench problem to retrieval attempt + classification (hit/miss/web)
- Score correctness (exact answer match) & reasoning quality (step alignment) using rule-based heuristics + optional embedding similarity.
### Metrics
- Retrieval Hit Rate
- Correctness Rate (KB vs Web vs Not Found)
- Confidence Calibration (score vs correctness)
### Script
`scripts/benchmark_jee.py` (to be implemented) will:
1. Load dataset subset
2. Loop queries → gather pipeline outputs
3. Aggregate metrics + export JSON/CSV report

## 8. Proposed Improvements Roadmap
| Phase | Focus | Deliverables |
|-------|-------|-------------|
| 1 | KB Expansion | Ingestion script + 200 problems |
| 2 | Web Search Upgrade | Tavily integration + MCP workflow hook |
| 3 | Feedback → KB | Auto promote high-quality corrections |
| 4 | Benchmark | JEE Bench script + results summary |
| 5 | Optimization | DSPy iterative refinement cycle |
| 6 | Deliverables | PDF proposal + architecture diagram + demo video |

## 9. Risk Analysis & Mitigation
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Small KB coverage | Low internal answer quality | Expand dataset + curation tooling |
| Single search provider | Dependency / outages | Add backup provider & caching |
| Limited HITL learning | Plateau in quality | Automate correction ingestion & DSPy cycles |
| Open endpoints | Abuse potential | Add API key + rate limiting + scoped admin routes |
| Sparse benchmarking | Hard to quantify progress | Implement JEE Bench evaluation early |

## 10. Deliverables Checklist
| Item | Status |
|------|--------|
| Source Code (FastAPI + React) | ✅ |
| Guardrails Implementation | ✅ |
| Knowledge Base & Vector Search | ✅ (seed) |
| Web Search / External Retrieval | ⚠️ (Perplexity only) |
| MCP Usage | ⚠️ (Server ready, workflow integration pending) |
| HITL Feedback System | ✅ |
| DSPy Integration | ✅ (analytics) |
| Benchmark Script | ❌ (planned) |
| Proposal PDF | ❌ (to generate from this draft) |
| Demo Video | ❌ (to produce) |
| Architecture Diagram | ⚠️ (text only) |

## 11. Next Immediate Actions
1. Integrate MCP tool calls into LangGraph workflow for retrieval augmentation.
2. Add Tavily web search fallback when Perplexity confidence low or API unavailable.
3. Implement benchmark script + initial JEE Bench subset evaluation.
4. Generate proposal PDF (e.g., `pandoc PROPOSAL_DRAFT.md -o Proposal.pdf`).
5. Create Mermaid diagram & export.
6. Strengthen auth (API key header + rate limiting).

## 12. Conclusion
The project scaffolds a functional Agentic RAG Math Assistant with core routing, guardrails, and feedback. To achieve full compliance with the assignment, priority is MCP integration, KB scaling, benchmarking, and formal deliverables (PDF + video).

---
Generated: YYYY-MM-DD (update before PDF export)

