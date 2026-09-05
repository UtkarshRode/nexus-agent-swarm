import React, { useState } from 'react';
import { Code, Copy, Check, FileCode, Layers } from 'lucide-react';
import { useSwarm } from '../context/SwarmContext';

export const ArtifactViewer = () => {
  const { artifacts } = useSwarm();
  const fileNames = Object.keys(artifacts);
  const [selectedFile, setSelectedFile] = useState(fileNames[0] || null);
  const [copied, setCopied] = useState(false);

  // Default to first file if selection invalid
  const activeFileName = (fileNames.includes(selectedFile) ? selectedFile : fileNames[0]) || null;
  const activeArtifact = activeFileName ? artifacts[activeFileName] : null;

  const handleCopy = () => {
    if (!activeArtifact) return;
    navigator.clipboard.writeText(activeArtifact.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 sm:p-6 backdrop-blur-md shadow-xl flex flex-col h-[520px]">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <FileCode className="h-4 w-4 text-emerald-400" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Generated Workspace Artifacts ({fileNames.length} files)
          </h3>
        </div>
        {activeArtifact && (
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-all"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        )}
      </div>

      {/* Tabs */}
      {fileNames.length > 0 && (
        <div className="flex space-x-1 pt-3 pb-2 overflow-x-auto border-b border-slate-800/60 text-xs font-mono">
          {fileNames.map((name) => (
            <button
              key={name}
              onClick={() => setSelectedFile(name)}
              className={`px-3 py-1.5 rounded-lg transition-all flex items-center space-x-1.5 ${
                activeFileName === name
                  ? 'bg-blue-600/20 text-blue-300 border border-blue-500/40 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <span>{name}</span>
              {artifacts[name].version > 1 && (
                <span className="text-[9px] px-1 py-0.2 rounded bg-purple-500/30 text-purple-200 font-bold">
                  v{artifacts[name].version}
                </span>
              )}
            </button>
          ))}
        </div>
      )}

      {/* Code Display */}
      <div className="flex-1 overflow-auto pt-3 font-mono text-xs">
        {activeArtifact ? (
          <pre className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-200 overflow-x-auto whitespace-pre leading-relaxed">
            <code>{activeArtifact.content}</code>
          </pre>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-slate-500 space-y-2">
            <Code className="h-8 w-8 text-slate-600 stroke-1" />
            <p>Artifacts produced by the Coder agent will compile here in real-time.</p>
          </div>
        )}
      </div>
    </div>
  );
};
