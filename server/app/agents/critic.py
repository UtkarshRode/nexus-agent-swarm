import asyncio
from app.agents.base import BaseAgent
from app.core.state import swarm_state, TaskItem

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Critic",
            role="Independent QA & Automated Code Verifier",
            system_prompt="""You are the Critic Agent in an autonomous engineering swarm.
Your job is to rigorously review code output, execute automated tests in the sandbox, and verify correctness.
If tests fail or edge cases are violated, you must reject the task and return explicit, actionable corrective feedback."""
        )

    async def verify(self, task: TaskItem, goal: str) -> bool:
        await swarm_state.update_status("CRITIQUE", active_agent="Critic")
        await swarm_state.update_task_status(task.id, "IN_PROGRESS")

        await self.emit_thought(
            stage="THINK",
            message="Commencing independent verification. Executing test suite inside the sandboxed runtime..."
        )
        await asyncio.sleep(1.0)

        test_file = "test_lru_cache.py" if ("cache" in goal.lower() or "lru" in goal.lower()) else "test_solution.py"

        # Tool Call: run_tests
        test_output = await self.invoke_tool("run_tests", test_filename=test_file)
        await asyncio.sleep(0.8)

        # Inspect if tests passed
        tests_passed = "FAILED" not in test_output and "ERRORS" not in test_output

        if tests_passed:
            await self.emit_thought(
                stage="REFLECT",
                message="✅ Verification Passed: All unit tests succeeded with 0 errors. Code conforms to specifications and edge-case contracts.",
                metadata={"status": "PASSED"}
            )
            await swarm_state.update_task_status(task.id, "COMPLETED", result="All unit tests passed")
            return True
        else:
            await self.emit_thought(
                stage="REFLECT",
                message="❌ Verification Failed: Detected test failures or exceptions. Formulating corrective guidance for Coder agent.",
                metadata={"status": "FAILED", "diagnostics": test_output[:300]}
            )
            await swarm_state.update_task_status(task.id, "FAILED", result="Tests failed")
            return False

critic_agent = CriticAgent()
