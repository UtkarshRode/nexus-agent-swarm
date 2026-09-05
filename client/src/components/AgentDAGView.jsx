import React from 'react';
import { ArrowRight, CheckCircle2, Clock, AlertCircle, ShieldAlert, Cpu, Terminal, FileCheck } from 'lucide-react';
import { useSwarm } from '../context/SwarmContext';

export const AgentDAGView = () => {
  const { tasks, activeAgent, status } = useSwarm();

  const agents = [
    {
      name: 'Supervisor',
      role: 'Planner & Task DAG',
      icon: Cpu,
      color: 'border-purple-500/40 bg-purple-950/20 text-purple-300',
      activeColor: 'border-purple-400 bg-purple-950/40 shadow-lg shadow-purple-500/20 ring-1 ring-purple-400',
    },
    {
      name: 'Coder',
      role: 'Tool & Code Execution',
      icon: Terminal,
      color: 'border-blue-500/40 bg-blue-950/20 text-blue-300',
      activeColor: 'border-blue-400 bg-blue-950/40 shadow-lg shadow-blue-500/20 ring-1 ring-blue-400',
    },
    {
      name: 'Critic',
      role: 'Verification & Self-Healing',
      icon: FileCheck,
      color: 'border-emerald-500/40 bg-emerald-950/20 text-emerald-300',
      activeColor: 'border-emerald-400 bg-emerald-950/40 shadow-lg shadow-emerald-500/20 ring-1 ring-emerald-400',
    },
  ];

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 sm:p-6 backdrop-blur-md shadow-xl space-y-6">
      {/* Visual Agent Pipeline */}
      <div>
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-2">
          <span>Autonomous Multi-Agent Topology</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 relative">
          {agents.map((agent, index) => {
            const Icon = agent.icon;
            const isActive = activeAgent === agent.name && status !== 'IDLE' && status !== 'COMPLETED';

            return (
              <div
                key={agent.name}
                className={`p-4 rounded-xl border transition-all duration-300 flex items-center justify-between ${
                  isActive ? agent.activeColor : agent.color
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg bg-slate-950/60 border border-slate-800`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="flex items-center space-x-1.5">
                      <span className="font-bold text-sm text-white">{agent.name}</span>
                      {isActive && (
                        <span className="h-2 w-2 rounded-full bg-blue-400 animate-ping" />
                      )}
                    </div>
                    <p className="text-[11px] text-slate-400">{agent.role}</p>
                  </div>
                </div>

                {index < 2 && (
                  <ArrowRight className="h-4 w-4 text-slate-600 hidden md:block" />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Decomposed Tasks List */}
      {tasks.length > 0 && (
        <div className="border-t border-slate-800/80 pt-5 space-y-3">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Decomposed Task Execution Pipeline ({tasks.filter(t => t.status === 'COMPLETED').length}/{tasks.length})
          </h4>
          <div className="space-y-2">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono transition-all ${
                  task.status === 'COMPLETED'
                    ? 'bg-slate-950/60 border-emerald-500/30 text-emerald-300'
                    : task.status === 'IN_PROGRESS'
                    ? 'bg-blue-950/30 border-blue-500/40 text-blue-200'
                    : 'bg-slate-950/40 border-slate-800 text-slate-400'
                }`}
              >
                <div className="flex items-center space-x-2.5">
                  {task.status === 'COMPLETED' && <CheckCircle2 className="h-4 w-4 text-emerald-400" />}
                  {task.status === 'IN_PROGRESS' && <Clock className="h-4 w-4 text-blue-400 animate-spin" />}
                  {task.status === 'PENDING' && <div className="h-2 w-2 rounded-full bg-slate-600 ml-1 mr-1" />}
                  <span className="font-semibold">{task.title}</span>
                </div>

                <div className="flex items-center space-x-2">
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">
                    {task.assigned_agent}
                  </span>
                  <span
                    className={`text-[10px] uppercase px-2 py-0.5 rounded font-bold ${
                      task.status === 'COMPLETED'
                        ? 'bg-emerald-500/10 text-emerald-400'
                        : task.status === 'IN_PROGRESS'
                        ? 'bg-blue-500/10 text-blue-400 animate-pulse'
                        : 'text-slate-500'
                    }`}
                  >
                    {task.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
