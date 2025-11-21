# Requirements Coverage Report

This document maps the assignment instructions to the current implementation and highlights gaps & next steps.

## Legend
- ✅ Implemented
- ⚠️ Partial / Needs Improvement
- ❌ Missing

## 1. Core Agentic RAG Flow
| Requirement | Status | Notes |
|-------------|--------|-------|
| Math question routing (KB → web search) | ⚠️ | KB search implemented (Qdrant in-memory). Web search via Perplexity only (single model). Added internal KB answer path. Need richer search (Tavily/Serper) & MCP integration in main workflow. |
| Step-by-step solution from KB match | ✅ | Now returns structured steps via `kb_internal` source. |
| Fallback to web search if not in KB | ✅ | Perplexity web search used; citations appended when available. |
| Avoid incorrect results when not found | ⚠️ | Not-found handler returns guidance; could add explicit confidence + suggestion to rephrase & no fabricated answer guarantee. |

## 2. Guardrails (AI Gateway)
| Requirement | Status | Notes |
| Input guardrails (math-only) | ✅ | Extensive keyword/symbol/harm filters. |
| Output guardrails (safety + sanitization) | ✅ | Harmful patterns, low-quality detection, sanitization of URLs/emails/phones. |
| Privacy considerations | ⚠️ | Basic sanitization; no PII redaction beyond URLs/emails/phones. Could add more (names, addresses). |

## 3. Knowledge Base
| Requirement | Status | Notes |
| Vector DB usage | ✅ | Qdrant in-memory collection with sentence-transformers embedding. |
| Dataset selection | ⚠️ | Only 5 sample problems embedded; needs larger curated math dataset (e.g., JEE Bench subset or open math QA). |
| Retrieval confidence scoring | ✅ | Implemented (none/low/medium/high). |
| KB expansion scripts | ⚠️ | Scripts exist (`populate_kb.py`, `expand_kb.py`), but not integrated in pipeline; no auto-update from feedback yet. |

## 4. Web Search / MCP
| Requirement | Status | Notes |
| Web search pipeline | ⚠️ | Perplexity used for combined search + generation; no multi-source extraction. |
| MCP usage (MUST) | ⚠️ | MCP server exists (`mcp_server.py`) exposing KB tools, but main workflow does not call MCP tools. Need integration. |
| Structured extraction strategy | ❌ | No parsing of retrieved documents; rely on LLM answer. |

## 5. Human-in-the-Loop (HITL)
| Requirement | Status | Notes |
| Feedback capture | ✅ | `/feedback/submit` and related endpoints; JSON persistence. |
| Feedback analytics | ✅ | Stats, improvement suggestions, problem status. |
| Learning from feedback | ⚠️ | DSPy scaffolding analyzes patterns; no model fine-tuning or prompt re-writing executed yet. |
| Incorporate corrections | ⚠️ | Stored but not reinjected into KB automatically. |

## 6. Bonus: DSPy Usage
| Requirement | Status | Notes |
| DSPy integration for optimization | ✅ | Basic optimizer producing recommendations. No training loop yet. |

## 7. Bonus: JEE Bench Benchmark
| Requirement | Status | Notes |
| Benchmark script | ❌ | Not implemented. Placeholder needed. |
| Results reporting | ❌ | Not available. |

## 8. Final Proposal Deliverables
| Requirement | Status | Notes |
| Proposal PDF | ❌ | Not generated. Draft markdown pending. |
| Architecture flowchart | ⚠️ | Textual architecture docs exist (LANGGRAPH_PIPELINE_ARCHITECTURE.md) but no diagram export. |
| Demo video | ❌ | Not included. |
| Source code (FastAPI + React) | ✅ | Present; frontend build available. |
| Clear examples (KB vs web) | ⚠️ | Should document 2 KB-hit and 2 web-search queries explicitly. |

## 9. Code Quality / Extensibility
| Area | Status | Notes |
| Modular workflow (LangGraph) | ✅ | Graph compiled; now extended with internal KB branch. |
| Configuration via env vars | ⚠️ | Perplexity key only; no config abstraction for future search providers. |
| Tests | ⚠️ | Basic tests mock workflow; need real integration tests & guardrail tests. |
| Security | ⚠️ | Open CORS; no auth for admin endpoints. |

## 10. Gaps & Recommended Actions
1. Integrate MCP tools directly in workflow (use MCP client or direct Python import pattern to simulate MCP call for search enrichment).
2. Add multi-source web search (Tavily or Serper API) – separate retrieval then synthesis step.
3. Expand KB with >200 math problems; create ingestion pipeline & evaluate embeddings.
4. Auto-add high-quality user corrections into KB (review queue + admin approval).
5. Add JEE Bench benchmark script (`scripts/benchmark_jee.py`) + scoring metrics (accuracy, coverage, confidence alignment).
6. Generate Proposal PDF using `weasyprint` or `pandoc` from `PROPOSAL_DRAFT.md`.
7. Produce architecture diagram (Mermaid or draw.io export) and embed in docs.
8. Enhance DSPy integration: convert negative feedback into synthetic counterexamples & prompt refinement.
9. Implement rate limiting + simple API key auth for protected endpoints.
10. Improve not_found reasoning by returning explicit retrieval scores and suggestion to rephrase.

## 11. Quick Win Changes Already Applied
- Added `kb_internal` answer path for medium/high confidence matches.
- Response now includes `reasoning_steps` for internal KB answers.

## 12. Next Step Decision Points
| Decision | Options | Recommendation |
|----------|---------|----------------|
| Web Search Provider | Tavily / Serper / Exa / Perplexity only | Add Tavily (lightweight JSON API) |
| KB Storage | In-memory / persistent Qdrant | Switch to file-based or external Qdrant for persistence |
| Feedback Reinforcement | Passive view / active retraining | Implement correction-to-KB pipeline |
| Benchmarking | Manual spot check / automated script | Implement automated JEE Bench scoring |

## 13. Example Queries to Demonstrate Routing
| Type | Query | Expected Source |
|------|-------|-----------------|
| KB Hit | "Evaluate ∫₀¹ x² ln(x) dx" | kb_internal |
| KB Hit | "Find derivative of x^x" | kb_internal |
| Web Search | "Explain Cauchy-Schwarz inequality" | perplexity_web |
| Web Search | "Applications of Maclaurin series in physics" | perplexity_web |

## 14. Risk & Mitigation Summary
| Risk | Mitigation |
|------|------------|
| Single web search dependency | Add second provider + caching layer |
| Small KB coverage | Bulk ingestion + periodic embedding refresh |
| No auth / open endpoints | Add API key or JWT-based auth middleware |
| Limited feedback learning | Implement scheduled DSPy optimization cycle |
| Missing formal deliverables | Automate proposal + PDF generation pipeline |

## 15. Conclusion
The project implements core scaffolding (FastAPI, LangGraph workflow, guardrails, feedback system, KB with vector search, Perplexity fallback). It partially fulfills the assignment. To achieve full compliance, focus on MCP integration within active routing, richer web search, KB expansion, formal benchmarking, and deliverable generation (proposal PDF & demo video).

---

Generated: YYYY-MM-DD (update date on regeneration)

