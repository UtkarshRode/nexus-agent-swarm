import React, { useState } from 'react';
import { Send, Sparkles, Play, RotateCcw } from 'lucide-react';
import { useSwarm } from '../context/SwarmContext';

export const GoalInput = () => {
  const { executeGoal, isExecuting, status } = useSwarm();
  const [prompt, setPrompt] = useState('Build a high-performance LRU Cache with O(1) operations and full unit tests');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim() || isExecuting) return;
    executeGoal(prompt.trim());
  };

  const handleQuickPrompt = (preset) => {
    setPrompt(preset);
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-5 sm:p-6 backdrop-blur-xl shadow-xl space-y-4">
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isExecuting}
            placeholder="Instruct the autonomous agent swarm (e.g. Build an LRU Cache with tests)..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all font-mono"
          />
        </div>

        <button
          type="submit"
          disabled={isExecuting || !prompt.trim()}
          className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs sm:text-sm font-bold shadow-lg shadow-blue-900/30 flex items-center justify-center space-x-2 transition-all disabled:opacity-50 active:scale-95 flex-shrink-0"
        >
          {isExecuting ? (
            <>
              <RotateCcw className="h-4 w-4 animate-spin" />
              <span>Swarm Collaborating ({status})...</span>
            </>
          ) : (
            <>
              <Play className="h-4 w-4 fill-white" />
              <span>Deploy Autonomous Swarm</span>
            </>
          )}
        </button>
      </form>

      {/* Quick Prompt Presets */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-slate-400 text-[11px] font-semibold flex items-center space-x-1">
          <Sparkles className="h-3 w-3 text-blue-400" />
          <span>Quick Goals:</span>
        </span>
        <button
          onClick={() => handleQuickPrompt('Build a high-performance LRU Cache with O(1) operations and full unit tests')}
          disabled={isExecuting}
          className="px-2.5 py-1 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 transition-all hover:border-slate-700"
        >
          LRU Cache with Unit Tests
        </button>
        <button
          onClick={() => handleQuickPrompt('Implement a Token Bucket Rate Limiter with burst capacity and tests')}
          disabled={isExecuting}
          className="px-2.5 py-1 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 transition-all hover:border-slate-700"
        >
          Token Bucket Rate Limiter
        </button>
        <button
          onClick={() => handleQuickPrompt('Design an Event-Driven PubSub Message Bus with subscriber filter')}
          disabled={isExecuting}
          className="px-2.5 py-1 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 transition-all hover:border-slate-700"
        >
          PubSub Message Bus
        </button>
      </div>
    </div>
  );
};
