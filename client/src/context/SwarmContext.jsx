import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import axios from 'axios';

const SwarmContext = createContext(null);

const API_BASE = import.meta.env.VITE_API_URL || '';
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

  // Initialize SSE connection to FastAPI backend
  useEffect(() => {
    const sseUrl = `${API_BASE}/api/swarm/stream`;
    const eventSource = new EventSource(sseUrl);


    eventSource.onopen = () => {
      console.log('⚡ [SSE] Connected to NexusSwarm stream');
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

    eventSource.onerror = (err) => {
      console.warn('⚡ [SSE] Connection dropped, reconnecting...', err);
      setIsConnected(false);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Launch a new goal
  const executeGoal = async (goal, model = 'simulation') => {
    setIsExecuting(true);
    setUserGoal(goal);
    try {
      await axios.post('/api/swarm/execute', { goal, model });
    } catch (err) {
      console.error('Execution launch failed:', err);
      setIsExecuting(false);
    }
  };

  // Handle human-in-the-loop approval
  const resolveApproval = async (approvalId, approved) => {
    try {
      await axios.post('/api/swarm/approve', {
        approval_id: approvalId,
        approved,
      });
      setPendingApproval(null);
    } catch (err) {
      console.error('Approval resolution failed:', err);
    }
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
