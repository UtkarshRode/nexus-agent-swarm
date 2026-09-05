import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TaskItem(BaseModel):
    id: str
    title: str
    description: str
    assigned_agent: str
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    result: Optional[str] = None

class ThoughtItem(BaseModel):
    id: str
    agent: str  # Supervisor, Coder, Critic, System
    stage: str  # THINK, TOOL_CALL, TOOL_RESULT, REFLECT, APPROVAL
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S.%f")[:-3])

class ArtifactItem(BaseModel):
    filename: str
    content: str
    language: str = "python"
    version: int = 1
    updated_at: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

class ApprovalRequest(BaseModel):
    approval_id: str
    tool_name: str
    description: str
    parameters: Dict[str, Any]
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED

class SwarmState:
    def __init__(self):
        self.session_id: str = "default_session"
        self.status: str = "IDLE"  # IDLE, PLANNING, CODING, CRITIQUE, AWAITING_APPROVAL, COMPLETED, FAILED
        self.user_goal: str = ""
        self.tasks: List[TaskItem] = []
        self.current_task_id: Optional[str] = None
        self.thoughts: List[ThoughtItem] = []
        self.artifacts: Dict[str, ArtifactItem] = {}
        self.pending_approval: Optional[ApprovalRequest] = None
        self.active_agent: str = "System"
        self.listeners: List[asyncio.Queue] = []
        self.lock = asyncio.Lock()

    def reset(self, goal: str):
        self.user_goal = goal
        self.status = "PLANNING"
        self.tasks = []
        self.current_task_id = None
        self.thoughts = []
        self.artifacts = {}
        self.pending_approval = None
        self.active_agent = "Supervisor"

    async def add_thought(self, agent: str, stage: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        async with self.lock:
            thought = ThoughtItem(
                id=f"th_{len(self.thoughts) + 1}",
                agent=agent,
                stage=stage,
                message=message,
                metadata=metadata or {},
            )
            self.thoughts.append(thought)
            self.active_agent = agent
            await self._broadcast({"type": "thought", "data": thought.model_dump()})

    async def update_status(self, status: str, active_agent: Optional[str] = None):
        async with self.lock:
            self.status = status
            if active_agent:
                self.active_agent = active_agent
            await self._broadcast({"type": "status", "data": {"status": self.status, "active_agent": self.active_agent}})

    async def set_tasks(self, tasks: List[TaskItem]):
        async with self.lock:
            self.tasks = tasks
            await self._broadcast({"type": "tasks", "data": [t.model_dump() for t in self.tasks]})

    async def update_task_status(self, task_id: str, status: str, result: Optional[str] = None):
        async with self.lock:
            for task in self.tasks:
                if task.id == task_id:
                    task.status = status
                    if result:
                        task.result = result
                    break
            self.current_task_id = task_id
            await self._broadcast({"type": "tasks", "data": [t.model_dump() for t in self.tasks]})

    async def save_artifact(self, filename: str, content: str, language: str = "python"):
        async with self.lock:
            version = 1
            if filename in self.artifacts:
                version = self.artifacts[filename].version + 1
            
            artifact = ArtifactItem(
                filename=filename,
                content=content,
                language=language,
                version=version,
            )
            self.artifacts[filename] = artifact
            await self._broadcast({"type": "artifact", "data": artifact.model_dump()})

    async def request_approval(self, approval_id: str, tool_name: str, description: str, parameters: Dict[str, Any]):
        async with self.lock:
            self.pending_approval = ApprovalRequest(
                approval_id=approval_id,
                tool_name=tool_name,
                description=description,
                parameters=parameters,
            )
            self.status = "AWAITING_APPROVAL"
            await self._broadcast({"type": "approval_required", "data": self.pending_approval.model_dump()})

    async def resolve_approval(self, approval_id: str, approved: bool):
        async with self.lock:
            if self.pending_approval and self.pending_approval.approval_id == approval_id:
                self.pending_approval.status = "APPROVED" if approved else "REJECTED"
                resolution = self.pending_approval.status
                self.pending_approval = None
                await self._broadcast({"type": "approval_resolved", "data": {"approval_id": approval_id, "status": resolution}})
                return approved
            return False

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self.listeners.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        if q in self.listeners:
            self.listeners.remove(q)

    async def _broadcast(self, event: Dict[str, Any]):
        for q in self.listeners:
            try:
                await q.put(event)
            except Exception:
                pass

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "status": self.status,
            "user_goal": self.user_goal,
            "active_agent": self.active_agent,
            "tasks": [t.model_dump() for t in self.tasks],
            "thoughts": [t.model_dump() for t in self.thoughts[-50:]],
            "artifacts": {k: v.model_dump() for k, v in self.artifacts.items()},
            "pending_approval": self.pending_approval.model_dump() if self.pending_approval else None,
        }

# Global singleton swarm state
swarm_state = SwarmState()
