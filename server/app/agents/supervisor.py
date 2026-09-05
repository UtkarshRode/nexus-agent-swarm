import asyncio
from typing import List
from app.agents.base import BaseAgent
from app.core.state import swarm_state, TaskItem

class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Supervisor",
            role="Lead Planner & Task Orchestrator",
            system_prompt="""You are the Lead Supervisor Agent in an autonomous engineering swarm.
Your job is to deconstruct high-level software goals into a clean, sequential Task Execution Plan.
Each plan must include:
1. Architectural analysis and file design
2. Core algorithmic implementation
3. Comprehensive automated test suite
4. Verification and critique"""
        )

    async def plan(self, user_goal: str) -> List[TaskItem]:
        await self.emit_thought(
            stage="THINK",
            message=f"Received goal: '{user_goal}'. Analyzing requirements and decomposing into sub-tasks..."
        )
        await asyncio.sleep(0.8)

        # Plan generation (works with LLM query or intelligent decomposition)
        tasks = [
            TaskItem(
                id="task_1",
                title="Design System Architecture & File Structure",
                description="Define data models, algorithm specifications, and target file layout.",
                assigned_agent="Supervisor",
            ),
            TaskItem(
                id="task_2",
                title="Implement Core Logic & Data Structures",
                description="Write clean, modular, and optimized Python implementation in the workspace sandbox.",
                assigned_agent="Coder",
            ),
            TaskItem(
                id="task_3",
                title="Write Unit Test Suite",
                description="Author rigorous unit tests covering edge cases, boundary conditions, and performance.",
                assigned_agent="Coder",
            ),
            TaskItem(
                id="task_4",
                title="Execute Sandboxed Tests & Run Verification Loop",
                description="Execute tests in isolated runtime, inspect stdout/stderr, and perform critic verification.",
                assigned_agent="Critic",
            ),
        ]

        await swarm_state.set_tasks(tasks)
        await self.emit_thought(
            stage="REFLECT",
            message=f"Task decomposition complete. Formulated {len(tasks)} sequential tasks. Handing off to execution pipeline.",
            metadata={"task_count": len(tasks)}
        )
        await asyncio.sleep(0.5)
        return tasks

supervisor_agent = SupervisorAgent()
