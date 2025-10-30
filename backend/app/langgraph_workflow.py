"""
LangGraph Workflow for Agentic RAG Math Agent
Orchestrates the decision flow: DB Search → Gemini Analysis → Web Search → Not Found
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
    gemini_response: str
    perplexity_response: str
    final_answer: str
    source: str
    note: str
    error: str


class MathRAGWorkflow:
    """LangGraph workflow for math problem solving"""
    
    def __init__(self, kb, gemini_fn, perplexity_fn):
        """
        Initialize workflow with dependencies
        
        Args:
            kb: Knowledge base instance
            gemini_fn: Function to call Gemini API
            perplexity_fn: Function to call Perplexity API
        """
        self.kb = kb
        self.gemini_fn = gemini_fn
        self.perplexity_fn = perplexity_fn
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(RAGState)
        
        # Add nodes (steps in the workflow)
        workflow.add_node("search_database", self.search_database)
        workflow.add_node("gemini_analyze", self.gemini_analyze)
        workflow.add_node("web_search", self.web_search)
        workflow.add_node("not_found", self.not_found)
        
        # Define entry point
        workflow.set_entry_point("search_database")
        
        # Add conditional edges based on decision logic
        workflow.add_conditional_edges(
            "search_database",
            self.route_after_db_search,
            {
                "gemini_analyze": "gemini_analyze",  # Found in DB
                "web_search": "web_search"            # Not in DB
            }
        )
        
        # Gemini analysis leads to end
        workflow.add_edge("gemini_analyze", END)
        
        # Web search has conditional routing
        workflow.add_conditional_edges(
            "web_search",
            self.route_after_web_search,
            {
                "success": END,      # Found on web
                "not_found": "not_found"  # Not found anywhere
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
    
    def route_after_db_search(self, state: RAGState) -> Literal["gemini_analyze", "web_search"]:
        """
        Decision: Route based on DB search results
        """
        if state['kb_results'] and state['confidence_score'] >= 0.5:
            logger.info(f"🎯 [Decision] DB match found ({state['confidence_score']:.2%}) → Gemini Analysis")
            return "gemini_analyze"
        else:
            logger.info(f"⚠️ [Decision] No DB match → Web Search")
            return "web_search"
    
    def gemini_analyze(self, state: RAGState) -> RAGState:
        """
        Node 2: Gemini analyzes database match and creates answer
        """
        logger.info(f"🤖 [Node 2: Gemini Analyze] Analyzing DB match: {state['best_match'].get('problem_id')}")
        
        try:
            # Build context from database
            best_match = state['best_match']
            context = f"""
DATABASE MATCH FOUND (Similarity: {state['confidence_score']:.1%}):

Problem ID: {best_match.get('problem_id')}
Question: {best_match.get('question')}
Topic: {best_match.get('topic')}
Difficulty: {best_match.get('difficulty')}

Solution Steps from Database:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(best_match.get('solution_steps', [])))}

Final Answer: {best_match.get('final_answer')}

Tags: {', '.join(best_match.get('tags', []))}
"""
            
            # Call Gemini
            gemini_response = self.gemini_fn(state['question'], context)
            
            state['gemini_response'] = gemini_response
            state['final_answer'] = gemini_response
            state['source'] = 'gemini_with_db'
            state['note'] = f"Answer analyzed and generated by Gemini based on database match (Problem: {best_match.get('problem_id')})"
            
            logger.info(f"✅ Gemini analysis complete")
            
        except Exception as e:
            logger.error(f"Error in Gemini analysis: {e}")
            state['error'] = str(e)
            state['final_answer'] = f"Error: {str(e)}"
        
        return state
    
    def web_search(self, state: RAGState) -> RAGState:
        """
        Node 3: Search the web using Perplexity
        """
        logger.info(f"🌐 [Node 3: Web Search] Searching web for: {state['question']}")
        
        try:
            # Call Perplexity
            perplexity_response = self.perplexity_fn(state['question'])
            
            state['perplexity_response'] = perplexity_response
            
            # Check if we got a valid response
            if perplexity_response and not any(err in perplexity_response.lower() 
                                               for err in ['failed', 'error', 'missing']):
                state['final_answer'] = perplexity_response
                state['source'] = 'perplexity_web'
                state['note'] = "Answer found via Perplexity web search (not in database)"
                logger.info(f"✅ Web search successful")
            else:
                state['final_answer'] = ""
                logger.info(f"❌ Web search failed or no results")
            
        except Exception as e:
            logger.error(f"Error in web search: {e}")
            state['error'] = str(e)
            state['final_answer'] = ""
        
        return state
    
    def route_after_web_search(self, state: RAGState) -> Literal["success", "not_found"]:
        """
        Decision: Route based on web search results
        """
        if state['final_answer'] and state['source'] == 'perplexity_web':
            logger.info(f"✅ [Decision] Web search successful → End")
            return "success"
        else:
            logger.info(f"❌ [Decision] Web search failed → Not Found")
            return "not_found"
    
    def not_found(self, state: RAGState) -> RAGState:
        """
        Node 4: Handle case when nothing is found
        """
        logger.info(f"❌ [Node 4: Not Found] No answer found anywhere")
        
        state['final_answer'] = "❌ NOT FOUND - This question could not be answered. The problem is not in our database and was not found on the web."
        state['confidence'] = 'none'
        state['confidence_score'] = 0.0
        state['source'] = 'not_found'
        state['note'] = "No match in database and no results from web search"
        
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
