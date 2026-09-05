import React, { createContext, useContext, useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { runClientSimulation } from '../services/simulation';

const SwarmContext = createContext(null);

const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '' : 'https://nexus-agent-swarm.onrender.com');
axios.defaults.baseURL = API_BASE;

export const SwarmProvider = ({ children }) => {
  const [status, setStatus] = useState('IDLE');
  const [activeAgent, setActiveAgent] = useState('System');
  const [userGoal, setUserGoal] = useState('');
  const [tasks, setTasks] = useState([]);
  const [thoughts, setThoughts] = useState([]);
  const [artifacts, setArtifacts] = useState({});
  const [pendingApproval, setPendingApproval] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);

  const approvalResolverRef = useRef(null);

  // Initialize SSE connection to FastAPI backend
  useEffect(() => {
    let eventSource = null;
    try {
      const sseUrl = `${API_BASE}/api/swarm/stream`;
      eventSource = new EventSource(sseUrl);

      eventSource.onopen = () => {
        console.log('⚡ [SSE] Connected to Axiom stream');
        setIsConnected(true);
      };

      eventSource.onmessage = (e) => {
        if (!e.data || e.data === ': ping') return;
        try {
          const payload = JSON.parse(e.data);
          const { type, data } = payload;

          if (type === 'init') {
            setStatus(data.status || 'IDLE');
            setActiveAgent(data.active_agent || 'System');
            setUserGoal(data.user_goal || '');
            setTasks(data.tasks || []);
            setThoughts(data.thoughts || []);
            setArtifacts(data.artifacts || {});
            setPendingApproval(data.pending_approval || null);
            if (data.status && data.status !== 'IDLE' && data.status !== 'COMPLETED' && data.status !== 'FAILED') {
              setIsExecuting(true);
            }
          } else if (type === 'thought') {
            setThoughts((prev) => [...prev, data]);
          } else if (type === 'tasks') {
            setTasks(data);
          } else if (type === 'status') {
            setStatus(data.status);
            if (data.active_agent) setActiveAgent(data.active_agent);
            if (data.status === 'COMPLETED' || data.status === 'FAILED') {
              setIsExecuting(false);
            }
          } else if (type === 'artifact') {
            setArtifacts((prev) => ({
              ...prev,
              [data.filename]: data,
            }));
          } else if (type === 'approval_required') {
            setPendingApproval(data);
          } else if (type === 'approval_resolved') {
            setPendingApproval(null);
          }
        } catch (err) {
          console.error('Failed to parse SSE event:', err);
        }
      };

      eventSource.onerror = () => {
        setIsConnected(false);
      };
    } catch (err) {
      console.warn('SSE connection initialization skipped:', err);
    }

    return () => {
      if (eventSource) eventSource.close();
    };
  }, []);

  // Launch a new goal
  const executeGoal = async (goal, model = 'simulation') => {
    setIsExecuting(true);
    setUserGoal(goal);
    setThoughts([]);
    setTasks([]);
    setArtifacts({});

    // 1. First attempt to call the FastAPI backend
    let launchedOnBackend = false;
    try {
      const res = await axios.post('/api/swarm/execute', { goal, model }, { timeout: 3000 });
      if (res.data && res.data.success) {
        launchedOnBackend = true;
      }
    } catch (err) {
      console.warn('FastAPI backend unavailable or sleeping. Running client-side swarm orchestration engine.', err);
    }

    // 2. If backend is not available or sleeping, run client simulation engine
    if (!launchedOnBackend) {
      try {
        await runClientSimulation({
          goal,
          onThought: (th) => setThoughts((prev) => [...prev, th]),
          onTasks: (t) => setTasks(t),
          onStatus: (st) => {
            setStatus(st.status);
            if (st.active_agent) setActiveAgent(st.active_agent);
          },
          onArtifact: (art) => setArtifacts((prev) => ({ ...prev, [art.filename]: art })),
          waitForApproval: (approvalData) => {
            return new Promise((resolve) => {
              setPendingApproval(approvalData);
              approvalResolverRef.current = resolve;
            });
          },
        });
      } catch (simErr) {
        console.error('Simulation error:', simErr);
      } finally {
        setIsExecuting(false);
      }
    }
  };

  // Handle human-in-the-loop approval
  const resolveApproval = async (approvalId, approved) => {
    if (approvalResolverRef.current) {
      approvalResolverRef.current(approved);
      approvalResolverRef.current = null;
    }
    try {
      await axios.post('/api/swarm/approve', {
        approval_id: approvalId,
        approved,
      });
    } catch (err) {
      // Handled gracefully in client simulation
    }
    setPendingApproval(null);
  };

  return (
    <SwarmContext.Provider
      value={{
        status,
        activeAgent,
        userGoal,
        tasks,
        thoughts,
        artifacts,
        pendingApproval,
        isConnected,
        isExecuting,
        executeGoal,
        resolveApproval,
      }}
    >
      {children}
    </SwarmContext.Provider>
  );
};

export const useSwarm = () => useContext(SwarmContext);
