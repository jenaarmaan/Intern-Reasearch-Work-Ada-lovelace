"use client";

import { useState, useRef } from 'react';
import './globals.css';

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [negativePrompt, setNegativePrompt] = useState("");
  const [controlType, setControlType] = useState("canny");
  const [numSamples, setNumSamples] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [results, setResults] = useState<string[]>([]);
  const [conditioning, setConditioning] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleGenerate = async () => {
    if (!selectedFile || !prompt) {
      alert("Please provide both a prompt and a source image.");
      return;
    }

    setIsGenerating(true);
    setResults([]);

    const formData = new FormData();
    formData.append("prompt", prompt);
    formData.append("negative_prompt", negative_prompt);
    formData.append("control_type", controlType);
    formData.append("num_samples", numSamples.toString());
    formData.append("image", selectedFile);

    try {
      // Assuming backend runs on 8000
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.success) {
        setResults(data.outputs.map((url: string) => `http://localhost:8000${url}`));
        setConditioning(`http://localhost:8000${data.conditioning}`);
      } else {
        alert("Generation failed: " + data.detail);
      }
    } catch (error) {
      console.error(error);
      alert("Error connecting to backend AI engine.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <main style={{ minHeight: '100vh', padding: '60px 20px', position: 'relative', zIndex: 10 }}>
      <header style={{ textAlign: 'center', marginBottom: '80px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '15px' }}>
          <span className="status-dot"></span>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#22c55e', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Engine Online</span>
        </div>
        <h1 className="glow-text" style={{ fontSize: '4.5rem', marginBottom: '10px' }}>Luminary AI</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.4rem', maxWidth: '800px', margin: '0 auto' }}>
          Unleash structural creativity with Stable Diffusion and ControlNet.
        </p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '40px', maxWidth: '1400px', margin: '0 auto' }}>
        {/* Control Panel */}
        <div className="glass-panel animate-fade" style={{ padding: '30px' }}>
          <h2 style={{ marginBottom: '25px', fontSize: '1.5rem' }}>Configuration</h2>
          
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Primary Prompt</label>
            <textarea 
              className="input-field" 
              placeholder="Describe what you want to see..."
              style={{ height: '100px', resize: 'none' }}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Negative Prompt</label>
            <input 
              type="text" 
              className="input-field" 
              placeholder="What should be excluded?"
              value={negativePrompt}
              onChange={(e) => setNegativePrompt(e.target.value)}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '30px' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Control Mode</label>
              <select 
                className="input-field" 
                value={controlType}
                onChange={(e) => setControlType(e.target.value)}
              >
                <option value="canny">Canny Edge</option>
                <option value="depth">Depth Map</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Samples</label>
              <input 
                type="number" 
                className="input-field" 
                min="1" 
                max="4"
                value={numSamples}
                onChange={(e) => setNumSamples(parseInt(e.target.value))}
              />
            </div>
          </div>

          <div 
            style={{ 
              border: '2px dashed var(--glass-border)', 
              borderRadius: '16px', 
              padding: '40px', 
              textAlign: 'center',
              cursor: 'pointer',
              marginBottom: '30px',
              backgroundImage: previewUrl ? `url(${previewUrl})` : 'none',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              position: 'relative',
              minHeight: '200px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
            onClick={() => fileInputRef.current?.click()}
          >
            {!previewUrl && <p style={{ color: 'var(--text-muted)' }}>Click to upload source image</p>}
            {previewUrl && <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.4)', borderRadius: '16px' }} />}
            {previewUrl && <p style={{ zIndex: 1, fontWeight: 600 }}>Change Image</p>}
            <input type="file" ref={fileInputRef} hidden onChange={handleFileChange} accept="image/*" />
          </div>

          <button 
            className="btn-primary" 
            style={{ width: '100%', fontSize: '1.1rem' }}
            onClick={handleGenerate}
            disabled={isGenerating}
          >
            {isGenerating ? "Synthesizing..." : "Generate Masterpiece"}
          </button>
        </div>

        {/* Results Panel */}
        <div className="animate-fade" style={{ animationDelay: '0.2s' }}>
          {results.length === 0 && !isGenerating && (
            <div className="glass-panel" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
              <div style={{ textAlign: 'center' }}>
                <p style={{ fontSize: '1.5rem', marginBottom: '10px' }}>Awaiting Synthesis</p>
                <p>Upload an image and provide a prompt to begin.</p>
              </div>
            </div>
          )}

          {isGenerating && (
            <div className="glass-panel" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <div className="glow-text" style={{ fontSize: '1.8rem', fontWeight: 600 }}>Processing Latent Space...</div>
            </div>
          )}

          {results.length > 0 && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              {results.map((url, idx) => (
                <div key={idx} className="glass-panel" style={{ padding: '10px', overflow: 'hidden' }}>
                  <img src={url} alt={`Result ${idx}`} style={{ width: '100%', borderRadius: '16px', display: 'block' }} />
                </div>
              ))}
              {conditioning && (
                <div className="glass-panel" style={{ padding: '10px', opacity: 0.7 }}>
                  <p style={{ fontSize: '0.8rem', marginBottom: '10px', textAlign: 'center', color: 'var(--text-muted)' }}>Conditioning Guide</p>
                  <img src={conditioning} alt="Conditioning" style={{ width: '100%', borderRadius: '16px', filter: 'grayscale(100%)' }} />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
