import React from 'react';
import { Bot, Cpu, Radio, Sparkles, Layers } from 'lucide-react';
import { useSwarm } from '../context/SwarmContext';

export const Navbar = () => {
  const { isConnected, activeAgent, status } = useSwarm();

  const getAgentColor = (agent) => {
    switch (agent) {
      case 'Supervisor':
        return 'bg-purple-500/20 text-purple-300 border-purple-500/30';
      case 'Coder':
        return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
      case 'Critic':
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
      default:
        return 'bg-slate-800 text-slate-400 border-slate-700';
    }
  };

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-tight text-white">NexusSwarm</span>
              <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                AI Agent Swarm
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Supervisor • Coder • Critic • ReAct Loops & Self-Correction
            </p>
          </div>
        </div>

        {/* Right Status Indicators */}
        <div className="flex items-center space-x-3">
          {/* Active Agent Badge */}
          {activeAgent && (
            <div className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg border text-xs font-semibold font-mono ${getAgentColor(activeAgent)}`}>
              <Cpu className="h-3.5 w-3.5" />
              <span>Agent: {activeAgent}</span>
            </div>
          )}

          {/* Swarm State Status */}
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300">
            <span
              className={`h-2 w-2 rounded-full ${
                isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-red-500'
              }`}
            />
            <span className="hidden md:inline">
              {status === 'IDLE' ? 'Ready' : `State: ${status}`}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
