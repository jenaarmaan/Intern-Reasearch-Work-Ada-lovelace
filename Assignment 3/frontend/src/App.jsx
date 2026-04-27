import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

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
        setError(response.data.error || 'Failed to generate');
      }
    } catch (err) {
      setError('Connection failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#0a0a0c', color: 'white', minHeight: '100vh', padding: '40px', fontFamily: 'sans-serif' }}>
      <h1>AQC-GA</h1>
      <div style={{ background: '#16161e', padding: '20px', borderRadius: '10px', maxWidth: '600px' }}>
        <textarea 
          value={prompt} 
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt..."
          style={{ width: '100%', height: '100px', background: 'transparent', color: 'white', border: '1px solid #333' }}
        />
        <button 
          onClick={handleGenerate} 
          disabled={loading}
          style={{ marginTop: '10px', padding: '10px 20px', background: '#8b5cf6', color: 'white', border: 'none', borderRadius: '5px' }}
        >
          {loading ? 'Generating...' : 'Generate Circuit'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Result</h3>
          <pre style={{ background: '#000', padding: '10px' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
