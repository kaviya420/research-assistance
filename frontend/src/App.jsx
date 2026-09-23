import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Upload, FileText, Activity, AlertTriangle, Lightbulb, Loader2, Network, X, Send, Bot, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = 'http://localhost:8000/api/papers';

function App() {
  const [papers, setPapers] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [isChatLoading, setIsChatLoading] = useState(false);
  
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchPapers();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const fetchPapers = async () => {
    try {
      const res = await axios.get(API_URL);
      setPapers(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setIsUploading(true);
    setError(null);
    try {
      await axios.post(`${API_URL}/upload`, formData);
      await fetchPapers();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload paper');
    } finally {
      setIsUploading(false);
      e.target.value = null; // Clear the input so identical files trigger onChange
    }
  };

  const deletePaper = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      await fetchPapers();
      setAnalysis(null); 
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete paper');
    }
  };

  const analyzePapers = async () => {
    setIsAnalyzing(true);
    try {
      const res = await axios.get(`${API_URL}/analyze`);
      setAnalysis(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze papers');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || isChatLoading) return;

    const query = chatInput.trim();
    setChatInput('');
    setChatMessages(prev => [...prev, { role: 'user', content: query }]);
    setIsChatLoading(true);

    try {
      const res = await axios.post(`${API_URL}/chat`, { query });
      setChatMessages(prev => [...prev, { role: 'assistant', content: res.data.answer }]);
    } catch (err) {
      setChatMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not retrieve answer from LLM.' }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans selection:bg-indigo-500 selection:text-white pb-32">
      <div className="max-w-6xl mx-auto space-y-8">
        
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-12">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent flex items-center gap-3">
              <Network className="w-10 h-10 text-indigo-400" />
              AI Research Assistant
            </h1>
            <p className="text-slate-400 mt-2 text-lg">Intelligent academic research analysis at your fingertips.</p>
          </div>
          <div className="flex items-center gap-4">
            <label className="relative cursor-pointer group">
              <input type="file" className="hidden" accept=".pdf" onChange={handleFileUpload} disabled={isUploading} />
              <div className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 transition-colors px-6 py-3 rounded-full font-medium shadow-lg shadow-indigo-500/20">
                {isUploading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Upload className="w-5 h-5" />}
                {isUploading ? 'Uploading...' : 'Upload Paper'}
              </div>
            </label>
            <button 
              onClick={analyzePapers}
              disabled={papers.length === 0 || isAnalyzing}
              className="flex items-center gap-2 bg-cyan-600 hover:bg-cyan-500 transition-colors px-6 py-3 rounded-full font-medium shadow-lg shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? <Loader2 className="w-5 h-5 animate-spin" /> : <Activity className="w-5 h-5" />}
              Analyze Synthesis
            </button>
          </div>
        </header>

        {error && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-xl flex items-center gap-3">
            <AlertTriangle className="w-5 h-5" />
            {error}
          </motion.div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 space-y-4">
            <h2 className="text-xl font-semibold flex items-center gap-2 mb-4 text-slate-200">
              <FileText className="w-5 h-5 text-indigo-400" />
              Uploaded Papers ({papers.length})
            </h2>
            <div className="space-y-3">
              <AnimatePresence>
                {papers.map((paper, i) => (
                  <motion.div 
                    key={paper.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ delay: i * 0.1 }}
                    className="glass p-4 rounded-xl hover:bg-white/5 transition-colors cursor-default relative group"
                  >
                    <button 
                      onClick={() => deletePaper(paper.id)}
                      className="absolute top-2 right-2 text-slate-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity p-1"
                      title="Remove paper"
                    >
                      <X className="w-4 h-4" />
                    </button>
                    <p className="font-medium text-slate-200 pr-6 truncate" title={paper.filename}>{paper.filename}</p>
                    <p className="text-sm text-slate-400 mt-1 line-clamp-2">{paper.summary?.abstract}</p>
                  </motion.div>
                ))}
              </AnimatePresence>
              {papers.length === 0 && (
                <div className="text-center p-8 border border-dashed border-slate-700 rounded-xl text-slate-500">
                  No papers uploaded yet. Please upload a PDF.
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-2 space-y-6">
            {!analysis && !isAnalyzing && (
              <div className="glass p-12 rounded-2xl flex flex-col items-center justify-center text-center border border-dashed border-slate-700 min-h-[400px]">
                <Activity className="w-16 h-16 text-slate-600 mb-4" />
                <h3 className="text-2xl font-medium text-slate-400">Awaiting Analysis</h3>
                <p className="text-slate-500 mt-2 max-w-md">Upload at least one paper and click "Analyze Synthesis" to uncover cross-references, contradictions, and topic clusters.</p>
              </div>
            )}
            
            {isAnalyzing && (
              <div className="glass p-12 rounded-2xl flex flex-col items-center justify-center text-center min-h-[400px]">
                <Loader2 className="w-16 h-16 text-indigo-500 animate-spin mb-4" />
                <h3 className="text-2xl font-medium text-indigo-400">Synthesizing Literature</h3>
                <p className="text-slate-400 mt-2">Deep-reading semantics, clustering topics, and mapping contradictions...</p>
              </div>
            )}

            {analysis && !isAnalyzing && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                <div className="glass p-6 rounded-2xl">
                  <h3 className="text-xl font-semibold mb-4 text-cyan-400 flex items-center gap-2">
                    <Network className="w-5 h-5" /> Topic Clusters
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {analysis.clusters.map((cluster, i) => (
                      <div key={i} className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
                        <h4 className="font-medium text-slate-200 mb-2">{cluster.cluster_name}</h4>
                        <ul className="list-disc pl-4 text-sm text-slate-400 space-y-1">
                          {cluster.documents.map((doc, j) => (
                            <li key={j} className="truncate" title={doc}>{doc}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="glass p-6 rounded-2xl">
                  <h3 className="text-xl font-semibold mb-4 text-yellow-400 flex items-center gap-2">
                    <Lightbulb className="w-5 h-5" /> Research Gaps
                  </h3>
                  <div className="bg-yellow-500/10 border border-yellow-500/20 p-5 rounded-xl text-yellow-100 whitespace-pre-wrap leading-relaxed">
                    {analysis.research_gaps}
                  </div>
                </div>

                <div className="glass p-6 rounded-2xl">
                  <h3 className="text-xl font-semibold mb-4 text-rose-400 flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5" /> Contradictions Detected
                  </h3>
                  <div className="bg-rose-500/10 border border-rose-500/20 p-5 rounded-xl text-rose-100 whitespace-pre-wrap leading-relaxed">
                    {analysis.contradictions}
                  </div>
                </div>
              </motion.div>
            )}
            
            <div className="glass rounded-2xl flex flex-col h-[500px] mt-8 border border-slate-700/50 shadow-2xl">
                <div className="p-4 border-b border-slate-800 bg-slate-900/50 rounded-t-2xl">
                    <h3 className="font-medium text-slate-200 flex items-center gap-2">
                        <Bot className="w-5 h-5 text-indigo-400" />
                        Chat with Papers (LLM Q&A)
                    </h3>
                    <p className="text-xs text-slate-400 mt-1">Ask questions directly about the uploaded documents.</p>
                </div>
                
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {chatMessages.length === 0 && (
                        <div className="h-full flex flex-col items-center justify-center text-slate-500 opacity-50">
                            <Bot className="w-12 h-12 mb-3" />
                            <p>Send a message to clarify any doubts!</p>
                        </div>
                    )}
                    {chatMessages.map((msg, i) => (
                        <motion.div 
                            key={i} 
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                        >
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-indigo-600' : 'bg-slate-700'}`}>
                                {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4 text-cyan-400" />}
                            </div>
                            <div className={`px-4 py-3 rounded-2xl max-w-[85%] text-sm leading-relaxed whitespace-pre-wrap ${msg.role === 'user' ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700'}`}>
                                {msg.content}
                            </div>
                        </motion.div>
                    ))}
                    {isChatLoading && (
                        <div className="flex gap-3">
                            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                                <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />
                            </div>
                            <div className="px-4 py-3 rounded-2xl bg-slate-800 text-slate-400 rounded-tl-none border border-slate-700 text-sm">
                                Searching documents and generating response...
                            </div>
                        </div>
                    )}
                    <div ref={chatEndRef} />
                </div>
                
                <div className="p-4 bg-slate-900/50 rounded-b-2xl border-t border-slate-800">
                    <form onSubmit={handleChatSubmit} className="relative flex items-center">
                        <input
                            type="text"
                            value={chatInput}
                            onChange={(e) => setChatInput(e.target.value)}
                            placeholder={papers.length > 0 ? "Ask me anything about these papers..." : "Upload papers first to enable chat"}
                            disabled={papers.length === 0 || isChatLoading}
                            className="w-full bg-slate-950 border border-slate-700 rounded-full pl-5 pr-12 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all disabled:opacity-50"
                        />
                        <button 
                            type="submit" 
                            disabled={!chatInput.trim() || papers.length === 0 || isChatLoading}
                            className="absolute right-2 p-2 bg-indigo-600 rounded-full text-white hover:bg-indigo-500 transition-colors disabled:opacity-50 disabled:hover:bg-indigo-600"
                        >
                            <Send className="w-4 h-4" />
                        </button>
                    </form>
                </div>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
