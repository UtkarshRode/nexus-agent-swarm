import React, { useEffect, useRef } from 'react';
import { Terminal, Cpu, CheckCircle2, Wrench, Sparkles, MessageSquare } from 'lucide-react';
import { useSwarm } from '../context/SwarmContext';

export const ThoughtStream = () => {
  const { thoughts, isExecuting } = useSwarm();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [thoughts]);

  const getAgentBadge = (agent) => {
    switch (agent) {
      case 'Supervisor':
        return 'text-purple-400 border-purple-500/30 bg-purple-500/10';
      case 'Coder':
        return 'text-blue-400 border-blue-500/30 bg-blue-500/10';
      case 'Critic':
        return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
      default:
        return 'text-slate-400 border-slate-700 bg-slate-800';
    }
  };

  const getStageBadge = (stage) => {
    switch (stage) {
      case 'TOOL_CALL':
        return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
      case 'TOOL_RESULT':
        return 'bg-slate-950 text-slate-300 border-slate-800';
      case 'REFLECT':
        return 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30';
      default:
        return 'bg-slate-900 text-slate-400 border-slate-800';
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 sm:p-6 backdrop-blur-md shadow-xl flex flex-col h-[520px]">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Terminal className="h-4 w-4 text-blue-400" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Real-Time ReAct Reasoning Trace ({thoughts.length} events)
          </h3>
        </div>
        {isExecuting && (
          <div className="flex items-center space-x-1.5 text-xs text-blue-400 font-mono">
            <span className="h-2 w-2 rounded-full bg-blue-400 animate-pulse" />
            <span>Streaming Live...</span>
          </div>
        )}
      </div>

      {/* Thought Log Body */}
      <div className="flex-1 overflow-y-auto pt-4 space-y-3 pr-1 font-mono text-xs">
        {thoughts.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-500 space-y-2">
            <MessageSquare className="h-8 w-8 text-slate-600 stroke-1" />
            <p>Deploy a goal above to watch the multi-agent swarm think and execute tools.</p>
          </div>
        ) : (
          thoughts.map((item) => (
            <div
              key={item.id}
              className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-1.5 transition-all"
            >
              <div className="flex items-center justify-between text-[10px]">
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-0.5 rounded border font-semibold ${getAgentBadge(item.agent)}`}>
                    {item.agent}
                  </span>
                  <span className={`px-2 py-0.5 rounded border uppercase ${getStageBadge(item.stage)}`}>
                    {item.stage}
                  </span>
                </div>
                <span className="text-slate-500">{item.timestamp}</span>
              </div>

              <div className="text-slate-200 whitespace-pre-wrap leading-relaxed text-[11px] pt-1">
                {item.message}
              </div>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
