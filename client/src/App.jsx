import React from 'react';
import { Navbar } from './components/Navbar';
import { GoalInput } from './components/GoalInput';
import { AgentDAGView } from './components/AgentDAGView';
import { ThoughtStream } from './components/ThoughtStream';
import { ArtifactViewer } from './components/ArtifactViewer';
import { ApprovalModal } from './components/ApprovalModal';

export function App() {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col text-slate-100 font-sans">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Goal input bar */}
        <GoalInput />

        {/* Multi-Agent state & task DAG */}
        <AgentDAGView />

        {/* Two-column layout: Left = Live ReAct Thoughts, Right = Code Artifacts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ThoughtStream />
          <ArtifactViewer />
        </div>
      </main>

      {/* Human-in-the-loop permission gateway */}
      <ApprovalModal />

      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <p>NexusSwarm: Autonomous Multi-Agent Research & Code Swarm • SDE Placement Portfolio Project</p>
      </footer>
    </div>
  );
}

export default App;
