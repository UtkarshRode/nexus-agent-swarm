import React from 'react';
import { ShieldAlert, Check, X, AlertTriangle } from 'lucide-react';
import { useSwarm } from '../context/SwarmContext';

export const ApprovalModal = () => {
  const { pendingApproval, resolveApproval } = useSwarm();

  if (!pendingApproval) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-in fade-in duration-200">
      <div className="w-full max-w-md rounded-2xl border border-amber-500/40 bg-slate-900 p-6 shadow-2xl text-slate-100 relative space-y-4">
        {/* Header */}
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400 flex-shrink-0">
            <ShieldAlert className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Human-in-the-Loop Gateway</h3>
            <p className="text-xs text-amber-400/80">Permission required for tool execution</p>
          </div>
        </div>

        {/* Content */}
        <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2 text-xs font-mono">
          <div className="flex justify-between">
            <span className="text-slate-400">Tool:</span>
            <span className="text-amber-300 font-bold">{pendingApproval.tool_name}</span>
          </div>
          <div className="text-slate-300 pt-1">
            {pendingApproval.description}
          </div>
          <pre className="p-2 rounded bg-slate-900 text-[11px] text-slate-400 overflow-x-auto">
            {JSON.stringify(pendingApproval.parameters, null, 2)}
          </pre>
        </div>

        {/* Buttons */}
        <div className="flex space-x-3 pt-2">
          <button
            onClick={() => resolveApproval(pendingApproval.approval_id, false)}
            className="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-all flex items-center justify-center space-x-1.5"
          >
            <X className="h-4 w-4" />
            <span>Reject Tool</span>
          </button>

          <button
            onClick={() => resolveApproval(pendingApproval.approval_id, true)}
            className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold transition-all shadow-lg shadow-emerald-900/30 flex items-center justify-center space-x-1.5"
          >
            <Check className="h-4 w-4" />
            <span>Authorize Execution</span>
          </button>
        </div>
      </div>
    </div>
  );
};
