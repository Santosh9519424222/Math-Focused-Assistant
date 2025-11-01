"""
LangGraph Workflow for Agentic RAG Math Agent
Orchestrates the decision flow: DB Search → Perplexity Analysis → Web Search → Not Found
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
import logging

logger = logging.getLogger(__name__)

# Define the state that will be passed between nodes
class RAGState(TypedDict):
    """State for the RAG workflow"""
    question: str
    difficulty: str
    kb_results: list
    confidence: str
    confidence_score: float
    best_match: dict
    perplexity_response: str
    final_answer: str
    source: str
    note: str
    error: str


class MathRAGWorkflow:
    """LangGraph workflow for math problem solving"""
    
    def __init__(self, kb, perplexity_fn):
        """
        Initialize workflow with dependencies
        
        Args:
            kb: Knowledge base instance
            perplexity_fn: Function to call Perplexity API
        """
        self.kb = kb
        self.perplexity_fn = perplexity_fn
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(RAGState)
        
        # Add nodes (steps in the workflow)
        workflow.add_node("search_database", self.search_database)
        workflow.add_node("perplexity_analyze", self.perplexity_analyze)
        workflow.add_node("not_found", self.not_found)
        
        # Define entry point
        workflow.set_entry_point("search_database")
        
        # Add conditional edges based on decision logic
        workflow.add_conditional_edges(
            "search_database",
            self.route_after_db_search,
            {
                "perplexity_analyze": "perplexity_analyze",  # Always go to Perplexity
            }
        )
        
        # Perplexity analysis has conditional routing
        workflow.add_conditional_edges(
            "perplexity_analyze",
            self.route_after_perplexity,
            {
                "success": END,      # Perplexity succeeded
                "not_found": "not_found"  # Perplexity failed
            }
        )
        
        # Not found leads to end
        workflow.add_edge("not_found", END)
        
        return workflow.compile()
    
    def search_database(self, state: RAGState) -> RAGState:
        """
        Node 1: Search knowledge base for similar problems
        """
        logger.info(f"🔍 [Node 1: DB Search] Searching for: {state['question']}")
        
        try:
            # Search KB
            kb_results = self.kb.search_similar(
                state['question'],
                top_k=3,
                score_threshold=0.5
            )
            
            # Calculate confidence
            confidence, best_score = self.kb.get_retrieval_confidence(kb_results)
            
            state['kb_results'] = kb_results
            state['confidence'] = confidence
            state['confidence_score'] = best_score
            
            if kb_results:
                state['best_match'] = kb_results[0]
                logger.info(f"✅ Found {len(kb_results)} matches. Best: {best_score:.2%}")
            else:
                logger.info(f"❌ No matches found in database")
            
        except Exception as e:
            logger.error(f"Error in database search: {e}")
            state['error'] = str(e)
        
        return state
    
    def route_after_db_search(self, state: RAGState) -> Literal["perplexity_analyze"]:
        """
        Decision: Always route to Perplexity (with or without DB context)
        """
        if state['kb_results'] and state['confidence_score'] >= 0.5:
            logger.info(f"🎯 [Decision] DB match found ({state['confidence_score']:.2%}) → Perplexity will analyze with DB context")
        else:
            logger.info(f"⚠️ [Decision] No DB match → Perplexity will search web")
        return "perplexity_analyze"
    
    def perplexity_analyze(self, state: RAGState) -> RAGState:
        """
        Node 2: Perplexity analyzes the question
        - If DB match exists: Perplexity analyzes with DB context
        - If no DB match: Perplexity does web search
        """
        if state['kb_results'] and state['confidence_score'] >= 0.5:
            # Case 1: Database match - ask Perplexity to analyze with context
            logger.info(f"🤖 [Node 2: Perplexity Analyze] Analyzing with DB context: {state['best_match'].get('problem_id')}")
            
            try:
                best_match = state['best_match']
                
                # Build enriched prompt with database context
                enriched_question = f"""I found this similar problem in my database:

**Database Problem:**
Question: {best_match.get('question')}
Topic: {best_match.get('topic')}
Difficulty: {best_match.get('difficulty')}

**Solution from Database:**
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(best_match.get('solution_steps', [])))}

**Final Answer:** {best_match.get('final_answer')}

**User's Question:** {state['question']}

Please analyze if this database solution applies to the user's question. If it's the same problem, explain the solution step-by-step. If it's different, solve the user's question step-by-step."""
                
                # Call Perplexity with DB context
                perplexity_response = self.perplexity_fn(enriched_question)
                
                state['perplexity_response'] = perplexity_response
                state['final_answer'] = perplexity_response
                state['source'] = 'perplexity_with_db'
                state['note'] = f"Answer generated by Perplexity AI based on database match (Problem: {best_match.get('problem_id')}, Confidence: {state['confidence_score']:.1%})"
                
                logger.info(f"✅ Perplexity analysis with DB context complete")
                
            except Exception as e:
                logger.error(f"Error in Perplexity analysis: {e}")
                state['error'] = str(e)
                state['final_answer'] = f"Error: {str(e)}"
        
        else:
            # Case 2: No database match - Perplexity web search
            logger.info(f"🌐 [Node 2: Perplexity Web Search] Searching web for: {state['question']}")
            
            try:
                # Call Perplexity for web search
                perplexity_response = self.perplexity_fn(state['question'])
                
                state['perplexity_response'] = perplexity_response
                state['final_answer'] = perplexity_response
                state['source'] = 'perplexity_web'
                state['note'] = "Answer found via Perplexity web search (not in database)"
                
                logger.info(f"✅ Perplexity web search complete")
                
            except Exception as e:
                logger.error(f"Error in Perplexity web search: {e}")
                state['error'] = str(e)
                state['final_answer'] = None
        
        return state
    
    def route_after_perplexity(self, state: RAGState) -> Literal["success", "not_found"]:
        """
        Decision: Route based on Perplexity results
        """
        if state['final_answer'] and not state.get('error'):
            logger.info(f"✅ [Decision] Perplexity successful → End")
            return "success"
        else:
            logger.info(f"❌ [Decision] Perplexity failed → Not Found")
            return "not_found"
    
    def not_found(self, state: RAGState) -> RAGState:
        """
        Node 3: Handle case when Perplexity fails
        """
        logger.info(f"❌ [Node 3: Not Found] No answer available")
        
        state['final_answer'] = """❌ **ANSWER NOT AVAILABLE**

This question could not be answered because:
- **Not in our database**: No similar problems found in the knowledge base
- **Web search unavailable**: Perplexity API could not retrieve information

**Recommendations:**
1. Try rephrasing your question
2. Check if it's a valid mathematics problem
3. Verify API connectivity

**Topics in our database:**
- Calculus (derivatives, integrals, limits)
- Algebra (equations, polynomials, factorization)
- Probability (statistics, distributions)
- Trigonometry (identities, equations)

*If this is a math problem in these topics, please try asking in a different way.*"""
        
        state['confidence'] = 'none'
        state['confidence_score'] = 0.0
        state['source'] = 'not_found'
        state['note'] = "Not in database and Perplexity API unavailable"
        
        return state
    
    def run(self, question: str, difficulty: str = "JEE_Main") -> dict:
        """
        Execute the workflow
        
        Args:
            question: Math question to solve
            difficulty: Difficulty level
            
        Returns:
            Final state with answer
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 Starting LangGraph Workflow")
        logger.info(f"Question: {question}")
        logger.info(f"{'='*60}\n")
        
        # Initial state
        initial_state = RAGState(
            question=question,
            difficulty=difficulty,
            kb_results=[],
            confidence='none',
            confidence_score=0.0,
            best_match={},
            gemini_response='',
            perplexity_response='',
            final_answer='',
            source='',
            note='',
            error=''
        )
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✨ Workflow Complete!")
        logger.info(f"Source: {final_state['source']}")
        logger.info(f"Confidence: {final_state['confidence']} ({final_state['confidence_score']:.2%})")
        logger.info(f"{'='*60}\n")
        
        return final_state
