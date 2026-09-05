import asyncio
from app.core.config import settings
from app.core.state import swarm_state
from app.agents.supervisor import supervisor_agent
from app.agents.coder import coder_agent
from app.agents.critic import critic_agent

class SwarmEngine:
    def __init__(self):
        self.is_running = False

    async def run(self, user_goal: str):
        if self.is_running:
            return {"error": "Swarm is already actively running a task."}

        self.is_running = True
        try:
            # 1. Initialize session and plan
            swarm_state.reset(user_goal)
            await swarm_state.add_thought(
                agent="System",
                stage="THINK",
                message=f"Initialized multi-agent swarm for goal: '{user_goal}'. Launching Supervisor Agent..."
            )

            # 2. Supervisor Plan Phase
            tasks = await supervisor_agent.plan(user_goal)

            # 3. Step 1: Design
            await swarm_state.update_task_status("task_1", "IN_PROGRESS")
            await supervisor_agent.emit_thought(
                stage="THINK",
                message="Specifying module architecture, type definitions, and algorithmic time/space constraints."
            )
            await asyncio.sleep(0.8)
            await swarm_state.update_task_status("task_1", "COMPLETED", result="Architecture specification finalized")

            # 4. Step 2: Implementation
            await coder_agent.execute_implementation(tasks[1], user_goal)

            # 5. Step 3: Test Suite Creation
            await coder_agent.execute_testing(tasks[2], user_goal)

            # 6. Step 4: Critic Verification & Self-Correction Loop
            attempts = 0
            verified = False

            while attempts < settings.MAX_SELF_CORRECTION_LOOPS and not verified:
                attempts += 1
                verified = await critic_agent.verify(tasks[3], user_goal)
                
                if not verified and attempts < settings.MAX_SELF_CORRECTION_LOOPS:
                    await swarm_state.add_thought(
                        agent="System",
                        stage="REFLECT",
                        message=f"Initiating Self-Correction Loop {attempts + 1}/{settings.MAX_SELF_CORRECTION_LOOPS}: Re-dispatching to Coder with Critic feedback."
                    )
                    # Re-trigger Coder to fix defects
                    await coder_agent.execute_implementation(tasks[1], user_goal)

            if verified:
                await swarm_state.update_status("COMPLETED", active_agent="System")
                await swarm_state.add_thought(
                    agent="System",
                    stage="REFLECT",
                    message=f"🏆 Swarm Goal Achieved: All tasks completed, tests verified, and deliverables compiled in the Artifacts tab.",
                    metadata={"status": "SUCCESS"}
                )
            else:
                await swarm_state.update_status("FAILED", active_agent="System")
                await swarm_state.add_thought(
                    agent="System",
                    stage="REFLECT",
                    message="Swarm completed with unresolved issues after maximum self-correction attempts.",
                    metadata={"status": "FAILED"}
                )

        except Exception as e:
            await swarm_state.update_status("FAILED", active_agent="System")
            await swarm_state.add_thought(
                agent="System",
                stage="REFLECT",
                message=f"Swarm engine encountered unhandled runtime exception: {str(e)}"
            )
        finally:
            self.is_running = False

swarm_engine = SwarmEngine()
