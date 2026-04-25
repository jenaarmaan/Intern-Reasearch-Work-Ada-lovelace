import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Activity, Cpu, Code, Play, CheckCircle2, AlertCircle } from 'lucide-react';

const API_URL = 'http://localhost:8000';

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/generate`, { prompt });
      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || 'Failed to generate circuit');
      }
    } catch (err) {
      setError('Connection to backend failed. Make sure the server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-12 flex flex-col items-center">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-6xl font-bold mb-4 tracking-tight">
          AQC-<span className="gradient-text">GA</span>
        </h1>
        <p className="text-slate-400 text-lg">AI-Powered Quantum Circuit Generation & Analysis</p>
      </motion.div>

      {/* Prompt Input */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-3xl glass-card mb-8"
      >
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-2 text-slate-400 mb-2">
            <Sparkles size={18} className="text-purple-400" />
            <span className="text-sm font-medium uppercase tracking-wider">Describe your circuit</span>
          </div>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Create a Bell state with measurement..."
            className="w-full bg-transparent border-none text-xl text-slate-200 placeholder:text-slate-600 focus:ring-0 resize-none h-24 custom-scrollbar"
          />
          <div className="flex justify-between items-center mt-4">
            <div className="text-xs text-slate-500">
              Powered by Gemini & Qiskit
            </div>
            <button
              onClick={handleGenerate}
              disabled={loading || !prompt}
              className={`flex items-center gap-2 px-8 py-3 rounded-full font-semibold transition-all ${
                loading || !prompt 
                ? 'bg-slate-800 text-slate-500' 
                : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:shadow-[0_0_20px_rgba(139,92,246,0.4)]'
              }`}
            >
              {loading ? 'Processing...' : (
                <>
                  <Play size={18} fill="currentColor" />
                  Generate Circuit
                </>
              )}
            </button>
          </div>
        </div>
      </motion.div>

      {/* Results Section */}
      <AnimatePresence>
        {error && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="w-full max-w-3xl p-4 mb-6 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center gap-3 text-red-400"
          >
            <AlertCircle size={20} />
            {error}
          </motion.div>
        )}

        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            {/* Left: Circuit & Code */}
            <div className="flex flex-col gap-6">
              <div className="glass-card">
                <div className="flex items-center gap-2 mb-4 text-slate-300">
                  <Code size={18} className="text-blue-400" />
                  <span className="font-semibold">Circuit JSON (IR)</span>
                </div>
                <pre className="bg-black/40 p-4 rounded-lg text-xs text-blue-300 overflow-x-auto custom-scrollbar">
                  {JSON.stringify(result.circuit_json, null, 2)}
                </pre>
              </div>

              <div className="glass-card">
                <div className="flex items-center gap-2 mb-4 text-slate-300">
                  <Activity size={18} className="text-emerald-400" />
                  <span className="font-semibold">QASM Code</span>
                </div>
                <pre className="bg-black/40 p-4 rounded-lg text-xs text-slate-400 overflow-x-auto h-48 custom-scrollbar">
                  {result.qasm}
                </pre>
              </div>
            </div>

            {/* Right: Metrics & Results */}
            <div className="flex flex-col gap-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="glass-card flex flex-col items-center justify-center py-6">
                  <Cpu size={24} className="text-purple-400 mb-2" />
                  <div className="text-2xl font-bold">{result.metrics.depth}</div>
                  <div className="text-xs text-slate-500 uppercase tracking-widest">Depth</div>
                </div>
                <div className="glass-card flex flex-col items-center justify-center py-6">
                  <CheckCircle2 size={24} className="text-blue-400 mb-2" />
                  <div className="text-2xl font-bold">{result.metrics.gate_count}</div>
                  <div className="text-xs text-slate-500 uppercase tracking-widest">Gates</div>
                </div>
              </div>

              <div className="glass-card flex-grow">
                <div className="flex items-center gap-2 mb-6 text-slate-300">
                  <Activity size={18} className="text-purple-400" />
                  <span className="font-semibold">Simulation Results</span>
                </div>
                <div className="space-y-4">
                  {Object.entries(result.results).map(([state, count]) => (
                    <div key={state} className="group">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="font-mono text-slate-300">|{state}⟩</span>
                        <span className="text-slate-500">{(count/1024*100).toFixed(1)}% ({count})</span>
                      </div>
                      <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${(count/1024*100)}%` }}
                          className="h-full bg-gradient-to-r from-purple-500 to-blue-500"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Footer background effects */}
      <div className="fixed bottom-0 left-0 w-full h-1/2 -z-10 bg-gradient-to-t from-purple-900/10 to-transparent pointer-events-none" />
    </div>
  );
}

export default App;
