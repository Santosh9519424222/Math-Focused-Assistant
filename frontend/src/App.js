// React Frontend - Agentic RAG Math Agent

import React, { useState } from 'react';
import Tesseract from 'tesseract.js';
import './App.css';

// API URL from environment variable or fallback to production
// Check if process.env exists (build time) or use window location (runtime)
const API_URL = (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_URL) 
  ? process.env.REACT_APP_API_URL 
  : 'https://math-focused-assistant.onrender.com';

function App() {
  const [question, setQuestion] = useState('');
  const [difficulty, setDifficulty] = useState('JEE_Main');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [ocrProcessing, setOcrProcessing] = useState(false);
  const [ocrProgress, setOcrProgress] = useState(0);
  
  // Login modal state
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState(null);
  
  // HITL Feedback states
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [feedbackCorrection, setFeedbackCorrection] = useState('');
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  
  // User Problem Report states
  const [showProblemModal, setShowProblemModal] = useState(false);
  const [problemReport, setProblemReport] = useState({
    type: 'bug',
    description: '',
    email: ''
  });
  const [problemSubmitted, setProblemSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Create abort controller with 120 second timeout for first request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000); // 120 seconds
      
      const res = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, difficulty }),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);

      if (res.status === 401) {
        // Login required
        setShowLoginModal(true);
        setLoading(false);
        return;
      }

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
      // Reset feedback state for new query
      setFeedbackSubmitted(false);
      setFeedbackComment('');
      setFeedbackCorrection('');
      setShowFeedbackForm(false);
    } catch (err) {
      if (err.name === 'AbortError') {
        setError('Request timeout. The server is taking too long to respond. This usually happens on the first request while loading AI models. Please try again.');
      } else {
        setError(err.message || 'An error occurred while processing your request.');
      }
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle login
  const handleLogin = async () => {
    setLoginLoading(true);
    setLoginError(null);
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
      });
      if (!res.ok) {
        throw new Error('Login failed');
      }
      setShowLoginModal(false);
      setLoginLoading(false);
      setLoginError(null);
      // After login, user can submit again
      setTimeout(() => {
        setError(null);
      }, 500);
    } catch (err) {
      setLoginError('Login failed. Please try again.');
      setLoginLoading(false);
    }
  };

  // HITL Feedback submission
  const submitFeedback = async (rating) => {
    if (!response || !response.answer) return;

    try {
      const feedbackData = {
        question: question,
        answer: response.answer,
        rating: rating,
        correction: feedbackCorrection || null,
        comment: feedbackComment || null,
        metadata: {
          source: response.source,
          confidence: response.confidence,
          timestamp: new Date().toISOString()
        }
      };

      const res = await fetch(`${API_URL}/feedback/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
      });

      if (res.ok) {
        setFeedbackSubmitted(true);
        setTimeout(() => setFeedbackSubmitted(false), 3000);
        console.log('✓ Feedback submitted successfully');
      }
    } catch (err) {
      console.error('Error submitting feedback:', err);
    }
  };

  const getConfidenceBadge = (confidence) => {
    const badges = {
      high: { color: '#10b981', label: 'HIGH CONFIDENCE', icon: '✓' },
      medium: { color: '#f59e0b', label: 'MEDIUM CONFIDENCE', icon: '~' },
      low: { color: '#ef4444', label: 'LOW CONFIDENCE', icon: '!' },
      none: { color: '#6b7280', label: 'NO MATCH', icon: '×' }
    };
    const badge = badges[confidence] || badges.none;
    return (
      <span className="confidence-badge" style={{ backgroundColor: badge.color }}>
        {badge.icon} {badge.label}
      </span>
    );
  };

  const sampleQuestions = [
    'Evaluate the integral of x² ln(x) from 0 to 1',
    'Solve x³ - 3x + 2 = 0',
    'Find the derivative of x^x',
    'Probability of getting exactly 2 red balls',
    'What is the Maclaurin series for sin(x)?'
  ];

  // Math keyboard symbols organized by category
  const mathSymbols = {
    basic: ['×', '÷', '±', '∓', '≠', '≈', '∝'],
    powers: ['²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '⁰', 'ⁿ'],
    subscripts: ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉'],
    relations: ['≤', '≥', '<', '>', '=', '≡', '≢', '⊆', '⊇', '⊈', '⊉', '⊂', '⊃', '⊄', '⊅'],
    calculus: ['∫', '∂', '∇', '∆', 'Σ', '∏', 'lim', 'd/dx', '∫₀¹', '∫_{a}^{b}', '∑_{n=1}^{∞}', 'lim_{x→0}', 'dx', 'dy', 'dz', 'dt', '∫ f(x) dx', 'd/dx f(x)', '∂/∂x'],
    greek: ['α', 'β', 'γ', 'δ', 'θ', 'λ', 'μ', 'π', 'σ', 'φ', 'ω'],
    sets: ['∈', '∉', '⊂', '⊃', '∪', '∩', '∅', '∞', '⊆', '⊇', '⊄', '⊅', 'ℕ', 'ℤ', 'ℚ', 'ℝ', 'ℂ'],
    logic: ['∀', '∃', '∧', '∨', '¬', '⇒', '⇔', '⊥', '⊤'],
    special: ['√', '∛', '∜', '°', '%', '‰', '|', '∥', '∠', '△', '∘', 'π'],
    matrix: ['[ ]', '| |', 'det', 'Tr', 'rank', 'vec', 'A', 'B', 'C', 'D', 'E', 'F', 'G'],
    stats: ['𝔼', 'Var', 'Cov', 'P(A)', 'μ', 'σ', 'Σ', '∑', 'Pr', 'f(x)', 'g(x)', 'X', 'Y', 'Z'],
    geometry: ['∠', '△', '∘', 'π', '⊥', '∥', '∪', '∩', '∅', 'radius', 'diameter', 'area', 'volume'],
    latex: ['\frac{a}{b}', 'x^{n}', 'x_{i}', '\sqrt{x}', '\int f(x) dx', '\sum_{n=1}^{\infty}', '\lim_{x \to 0}', '\binom{n}{k}', '\log_{a}b', '\sin(x)', '\cos(x)', '\tan(x)']
  };

  const [showMathKeyboard, setShowMathKeyboard] = useState(false);
  const [activeCategory, setActiveCategory] = useState('basic');

  const insertSymbol = (symbol) => {
    setQuestion(prev => prev + symbol);
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      await processImage(file);
    }
  };

  const processImage = async (file) => {
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      setError('Image size should be less than 5MB');
      return;
    }
    
    setUploadedImage(file);
    setOcrProcessing(true);
    setOcrProgress(0);
    setError(null);
    
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
    
    // Perform OCR with improved settings for math
    try {
      const result = await Tesseract.recognize(
        file,
        'eng',
        {
          logger: (m) => {
            if (m.status === 'recognizing text') {
              setOcrProgress(Math.round(m.progress * 100));
            }
          },
          // Improved OCR settings for mathematical text
          tessedit_pageseg_mode: Tesseract.PSM.AUTO,
          tessedit_char_whitelist: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz()+-=*/^²³√∫∂∑∏πθαβγδεζηλμνξρσταφχψω.,?! ',
        }
      );
      
      let extractedText = result.data.text.trim();
      
      // Post-process OCR text to fix common math symbol errors
      extractedText = extractedText
        .replace(/®/g, 'x²')           // Fix ® → x²
        .replace(/@/g, 'x²')           // Fix @ → x²
        .replace(/\bsin\s+z\b/gi, 'sin x')  // Fix "sin z" → "sin x"
        .replace(/\bcos\s+z\b/gi, 'cos x')  // Fix "cos z" → "cos x"
        .replace(/\be\s*\^\s*x/gi, 'e^x')   // Fix "e ^ x" spacing
        .replace(/\bf\s*\(\s*z\s*\)/gi, 'f(x)')  // Fix f(z) → f(x)
        .replace(/\(\s*z\s*\)/g, '(x)')     // Fix (z) → (x)
        .replace(/\s+/g, ' ')               // Normalize whitespace
        .trim();
      
      if (extractedText) {
        // Replace question with extracted text
        setQuestion(extractedText);
        console.log('OCR extracted text (original):', result.data.text);
        console.log('OCR extracted text (cleaned):', extractedText);
      } else {
        setError('No text detected in image. Please type your question manually.');
        setQuestion('');
      }
      
    } catch (err) {
      console.error('OCR Error:', err);
      setError('Failed to extract text from image. Please type your question manually.');
    } finally {
      setOcrProcessing(false);
      setOcrProgress(0);
    }
  };

  const handlePaste = async (e) => {
    const items = e.clipboardData?.items;
    if (!items) return;

    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        e.preventDefault(); // Prevent default paste behavior
        const blob = items[i].getAsFile();
        if (blob) {
          await processImage(blob);
        }
        break;
      }
    }
  };

  const removeImage = () => {
    setUploadedImage(null);
    setImagePreview(null);
    setOcrProcessing(false);
    setOcrProgress(0);
    setQuestion('');
  };

  // Handle problem report submission
  const handleProblemSubmit = async (e) => {
    e.preventDefault();
    
    if (!problemReport.description.trim()) {
      alert('Please describe the problem');
      return;
    }

    try {
      const res = await fetch(`${API_URL}/feedback/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: `[USER PROBLEM REPORT - ${problemReport.type.toUpperCase()}]`,
          answer: problemReport.description,
          rating: 'thumbs_down',
          feedback_type: 'problem_report',
          comment: `Type: ${problemReport.type}\nEmail: ${problemReport.email || 'Not provided'}\n\nDescription: ${problemReport.description}`,
          correction: '',
          metadata: {
            source: 'user_problem_report',
            problem_type: problemReport.type,
            user_email: problemReport.email,
            timestamp: new Date().toISOString()
          }
        }),
      });

      if (res.ok) {
        setProblemSubmitted(true);
        setTimeout(() => {
          setShowProblemModal(false);
          setProblemSubmitted(false);
          setProblemReport({ type: 'bug', description: '', email: '' });
        }, 2000);
      }
    } catch (err) {
      console.error('Error submitting problem report:', err);
      alert('Failed to submit problem report. Please try again.');
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🧮 Agentic RAG Math Agent</h1>
        <p className="subtitle">Powered by Semantic Search & AI</p>
      </header>

      <main className="main-content">
        {/* Login Modal */}
        {showLoginModal && (
          <div className="modal-overlay" onClick={() => setShowLoginModal(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <h2>🔒 Login Required</h2>
                <button className="modal-close" onClick={() => setShowLoginModal(false)}>✕</button>
              </div>
              <div className="modal-body">
                <p>To continue, please log in. (Demo: Just click login to proceed)</p>
                {loginError && <div className="error-message">{loginError}</div>}
                <button className="btn-submit" onClick={handleLogin} disabled={loginLoading}>
                  {loginLoading ? 'Logging in...' : 'Login'}
                </button>
              </div>
            </div>
          </div>
        )}
        <div className="query-section">
          <div className="paste-hint">
            💡 <strong>Tip:</strong> Take a screenshot and press <kbd>Ctrl+V</kbd> to paste it directly, or click "📷 Upload & Scan". 
            <em>Note: OCR may need manual corrections for complex math notation.</em>
          </div>
          
          <form onSubmit={handleSubmit} className="query-form">
            <div className="input-group">
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onPaste={handlePaste}
                placeholder="Ask a math question... Type, paste image (Ctrl+V), or upload"
                className="question-input"
                rows="3"
                disabled={loading || ocrProcessing}
              />

              {ocrProcessing && (
                <div className="ocr-progress">
                  <div className="ocr-progress-bar">
                    <div 
                      className="ocr-progress-fill" 
                      style={{ width: `${ocrProgress}%` }}
                    ></div>
                  </div>
                  <p className="ocr-status">
                    📸 Scanning image and extracting text... {ocrProgress}%
                  </p>
                </div>
              )}

              {imagePreview && (
                <div className="image-preview-container">
                  <img src={imagePreview} alt="Uploaded problem" className="image-preview" />
                  <button
                    type="button"
                    className="remove-image-button"
                    onClick={removeImage}
                    disabled={loading || ocrProcessing}
                  >
                    ✕ Remove Image & Clear Text
                  </button>
                </div>
              )}
              
              <div className="form-controls">
                <div className="difficulty-selector">
                  <label>Difficulty:</label>
                  <select 
                    value={difficulty} 
                    onChange={(e) => setDifficulty(e.target.value)}
                    disabled={loading}
                  >
                    <option value="JEE_Main">JEE Main</option>
                    <option value="JEE_Advanced">JEE Advanced</option>
                  </select>
                </div>

                <label className="image-upload-button">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    disabled={loading || ocrProcessing}
                    style={{ display: 'none' }}
                  />
                  {ocrProcessing ? '⏳ Processing...' : '📷 Upload & Scan'}
                </label>
                
                <button
                  type="button"
                  className="math-keyboard-toggle"
                  onClick={() => setShowMathKeyboard(!showMathKeyboard)}
                  disabled={loading || ocrProcessing}
                >
                  {showMathKeyboard ? '✕ Close' : '∑ Math Keyboard'}
                </button>
                
                <button 
                  type="submit" 
                  className="submit-button"
                  disabled={loading || ocrProcessing || (!question.trim() && !uploadedImage)}
                >
                  {loading ? 'Searching...' : 'Get Answer'}
                </button>
              </div>
            </div>
          </form>

          {showMathKeyboard && (
            <div className="math-keyboard">
              <div className="keyboard-header">
                <h4>Mathematical Symbols</h4>
                <div className="category-tabs">
                  {Object.keys(mathSymbols).map((category) => (
                    <button
                      key={category}
                      className={`category-tab ${activeCategory === category ? 'active' : ''}`}
                      onClick={() => setActiveCategory(category)}
                    >
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </button>
                  ))}
                </div>
              </div>
              <div className="keyboard-symbols">
                {mathSymbols[activeCategory].map((symbol, idx) => (
                  <button
                    key={idx}
                    className="symbol-button"
                    onClick={() => insertSymbol(symbol)}
                    type="button"
                  >
                    {symbol}
                  </button>
                ))}
              </div>
              <div className="keyboard-info">
                <small>Click any symbol to insert it at the cursor position</small>
              </div>
            </div>
          )}

          <div className="sample-questions">
            <p className="sample-label">Try these examples:</p>
            <div className="sample-chips">
              {sampleQuestions.map((q, idx) => (
                <button
                  key={idx}
                  className="sample-chip"
                  onClick={() => setQuestion(q)}
                  disabled={loading}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
            <p>Make sure the backend server is running on {API_URL}</p>
          </div>
        )}

        {response && (
          <div className="response-section">
            <div className="response-header">
              <h2>Response</h2>
              {getConfidenceBadge(response.confidence)}
              <span className="source-badge">
                Source: {
                  response.source === 'knowledge_base' ? '📚 KB' : 
                  response.source === 'gemini_with_db' ? '🤖 Gemini + DB' :
                  response.source === 'gemini_rag' ? '🤖 Gemini RAG' : 
                  response.source === 'perplexity_web' ? '🌐 Web Search' :
                  response.source === 'not_found' ? '❌ Not Found' :
                  '🌐 External'
                }
              </span>
            </div>

            {response.confidence_score > 0 && (
              <div className="confidence-score">
                Similarity Score: {(response.confidence_score * 100).toFixed(1)}%
              </div>
            )}

            <div className="answer-box">
              <h3>Answer:</h3>
              <p className="answer-text" style={{ whiteSpace: 'pre-wrap' }}>{response.answer}</p>
            </div>

            {response.reasoning_steps && response.reasoning_steps.length > 0 && (
              <div className="solution-steps">
                <h3>Step-by-Step Solution:</h3>
                <ol>
                  {response.reasoning_steps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
              </div>
            )}

            {response.source === 'gemini_with_db' && response.note && (
              <div className="rag-info" style={{ borderColor: '#10b981', background: '#f0fdf4' }}>
                <h3>✅ Database Match Found - Gemini Analysis</h3>
                <p>{response.note}</p>
                <p className="context-info" style={{ background: '#d1fae5' }}>
                  📊 Matched Problem: {response.matched_problem_id} | Similarity: {(response.confidence_score * 100).toFixed(1)}%
                </p>
              </div>
            )}

            {response.source === 'gemini_rag' && response.note && (
              <div className="rag-info">
                <h3>🤖 AI-Generated Solution</h3>
                <p>{response.note}</p>
                {response.kb_results && response.kb_results.length > 0 && (
                  <p className="context-info">
                    ℹ️ Context provided from {response.kb_results.length} similar problem(s) in knowledge base
                  </p>
                )}
              </div>
            )}

            {response.source === 'perplexity_web' && response.note && (
              <div className="rag-info" style={{ borderColor: '#f59e0b', background: '#fffbeb' }}>
                <h3>🌐 Web Search Result</h3>
                <p>{response.note}</p>
                <p className="context-info" style={{ background: '#fef3c7' }}>
                  ⚠️ This problem was not found in our database - answer from web search
                </p>
              </div>
            )}

            {response.source === 'not_found' && (
              <div className="rag-info" style={{ borderColor: '#ef4444', background: '#fef2f2' }}>
                <h3>❌ Problem Not Found</h3>
                <p>{response.note}</p>
                {response.suggestion && (
                  <p className="context-info" style={{ background: '#fee2e2' }}>
                    💡 {response.suggestion}
                  </p>
                )}
              </div>
            )}

            {response.kb_results && response.kb_results.length > 0 && (
              <div className="kb-matches">
                <h3>Knowledge Base Matches:</h3>
                {response.kb_results.map((match, idx) => (
                  <div key={idx} className="kb-match-card">
                    <div className="match-header">
                      <span className="match-id">{match.problem_id}</span>
                      <span className="match-score">
                        {(match.score * 100).toFixed(1)}%
                      </span>
                    </div>
                    <p className="match-question">{match.question}</p>
                    <div className="match-meta">
                      <span className="match-topic">{match.topic}</span>
                      <span className="match-difficulty">{match.difficulty}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {response.matched_problem_id && (
              <div className="matched-problem">
                <strong>Matched Problem:</strong> {response.matched_problem_id}
                {response.topic && <span> | Topic: {response.topic}</span>}
                {response.difficulty && <span> | Level: {response.difficulty}</span>}
              </div>
            )}

            {response.external_sources && (
              <div className="external-sources">
                <h3>External API Responses:</h3>
                {Object.entries(response.external_sources).map(([api, resp]) => (
                  <div key={api} className="external-source">
                    <strong>{api}:</strong>
                    <p>{resp}</p>
                  </div>
                ))}
              </div>
            )}

            {/* HITL Feedback Section */}
            <div className="feedback-section">
              <h3>Was this response helpful?</h3>
              
              {!feedbackSubmitted ? (
                <div className="feedback-controls">
                  <div className="feedback-buttons">
                    <button 
                      className="feedback-btn thumbs-up"
                      onClick={() => submitFeedback('thumbs_up')}
                      title="This answer was helpful"
                    >
                      👍 Helpful
                    </button>
                    <button 
                      className="feedback-btn thumbs-down"
                      onClick={() => {
                        setShowFeedbackForm(true);
                        submitFeedback('thumbs_down');
                      }}
                      title="This answer needs improvement"
                    >
                      👎 Not Helpful
                    </button>
                  </div>

                  {showFeedbackForm && (
                    <div className="feedback-form">
                      <textarea
                        placeholder="Optional: Tell us what went wrong or provide the correct answer..."
                        value={feedbackComment}
                        onChange={(e) => setFeedbackComment(e.target.value)}
                        className="feedback-textarea"
                        rows="3"
                      />
                      <textarea
                        placeholder="Optional: Provide your correction/improvement..."
                        value={feedbackCorrection}
                        onChange={(e) => setFeedbackCorrection(e.target.value)}
                        className="feedback-textarea"
                        rows="3"
                      />
                      <button 
                        className="submit-feedback-btn"
                        onClick={() => {
                          submitFeedback('thumbs_down');
                          setShowFeedbackForm(false);
                        }}
                      >
                        Submit Detailed Feedback
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <div className="feedback-success">
                  ✅ Thank you for your feedback! This helps improve the system.
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Floating Problem Report Button */}
      <button 
        className="floating-problem-btn"
        onClick={() => setShowProblemModal(true)}
        title="Report a problem or give feedback"
      >
        🐛 Report Problem
      </button>

      {/* Problem Report Modal */}
      {showProblemModal && (
        <div className="modal-overlay" onClick={() => setShowProblemModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>📝 Report a Problem or Give Feedback</h2>
              <button 
                className="modal-close"
                onClick={() => setShowProblemModal(false)}
              >
                ✕
              </button>
            </div>

            {!problemSubmitted ? (
              <form onSubmit={handleProblemSubmit} className="problem-form">
                <div className="form-group">
                  <label htmlFor="problem-type">Problem Type:</label>
                  <select
                    id="problem-type"
                    value={problemReport.type}
                    onChange={(e) => setProblemReport({...problemReport, type: e.target.value})}
                    className="problem-select"
                  >
                    <option value="bug">🐛 Bug / Error</option>
                    <option value="feature">💡 Feature Request</option>
                    <option value="improvement">⚡ Improvement Suggestion</option>
                    <option value="ocr">📷 OCR Issue</option>
                    <option value="wrong_answer">❌ Wrong Answer</option>
                    <option value="other">📋 Other</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="problem-description">Description: *</label>
                  <textarea
                    id="problem-description"
                    value={problemReport.description}
                    onChange={(e) => setProblemReport({...problemReport, description: e.target.value})}
                    placeholder="Please describe the problem or your feedback in detail..."
                    className="problem-textarea"
                    rows="6"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="user-email">Email (optional):</label>
                  <input
                    id="user-email"
                    type="email"
                    value={problemReport.email}
                    onChange={(e) => setProblemReport({...problemReport, email: e.target.value})}
                    placeholder="your.email@example.com (if you want a response)"
                    className="problem-input"
                  />
                </div>

                <div className="modal-actions">
                  <button 
                    type="button" 
                    className="btn-cancel"
                    onClick={() => setShowProblemModal(false)}
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="btn-submit"
                  >
                    📤 Submit Report
                  </button>
                </div>

                <div className="status-link">
                  <a 
                    href={`${API_URL}/static/problem_status.html`}
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="view-status-link"
                  >
                    📊 View Problem Status & Resolution Progress
                  </a>
                </div>
              </form>
            ) : (
              <div className="problem-success">
                <div className="success-icon">✅</div>
                <h3>Thank You!</h3>
                <p>Your feedback has been submitted successfully.</p>
                <p className="success-note">We'll review it and work on improvements!</p>
                
                <div className="status-link" style={{marginTop: '20px'}}>
                  <a 
                    href={`${API_URL}/../problem_status.html`}
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="view-status-link"
                  >
                    📊 View All Problem Reports & Status
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <footer className="app-footer">
        <p>
          Agentic RAG Math Agent v1.0.0 | Powered by Qdrant + sentence-transformers<br />
          Developed by Santosh Yadav | Contact: santosh.951942@gmail.com<br />
          © 2025 Santosh Yadav. All rights reserved.
        </p>
      </footer>
    </div>
  );
}

export default App;