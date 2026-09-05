import json
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.core.state import swarm_state
from app.agents.engine import swarm_engine
from app.api.schemas import ExecuteGoalRequest, ApprovalActionRequest, StandardResponse

router = APIRouter(prefix="/api")

@router.get("/health")
def health_check():
    return {
        "status": "ONLINE",
        "service": "nexus-agent-swarm",
        "active_agent": swarm_state.active_agent,
    }

@router.get("/swarm/status")
def get_swarm_status():
    return {
        "success": True,
        "data": swarm_state.get_snapshot(),
    }

@router.post("/swarm/execute")
async def execute_swarm_goal(request: ExecuteGoalRequest, background_tasks: BackgroundTasks):
    if not request.goal.strip():
        raise HTTPException(status_code=400, detail="Goal prompt cannot be empty.")

    if swarm_engine.is_running:
        return {
            "success": False,
            "message": "Swarm is currently executing another task. Please wait or monitor stream.",
            "data": swarm_state.get_snapshot(),
        }

    # Launch swarm execution as an async background task
    background_tasks.add_task(swarm_engine.run, request.goal)

    return {
        "success": True,
        "message": f"Swarm launched for goal: '{request.goal}'",
        "data": {"status": "PLANNING"},
    }

@router.post("/swarm/approve")
async def resolve_approval(request: ApprovalActionRequest):
    resolved = await swarm_state.resolve_approval(request.approval_id, request.approved)
    if not resolved:
        raise HTTPException(status_code=404, detail="Approval ID not found or already processed.")

    return {
        "success": True,
        "message": f"Approval {request.approval_id} marked as {'APPROVED' if request.approved else 'REJECTED'}.",
    }

@router.get("/swarm/stream")
async def stream_swarm_events():
    """
    Server-Sent Events (SSE) streaming endpoint for real-time thought traces,
    tool call outputs, task transitions, and artifact compilation.
    """
    queue = swarm_state.subscribe()

    async def event_generator():
        # Send initial snapshot immediately upon connection
        initial_event = json.dumps({"type": "init", "data": swarm_state.get_snapshot()})
        yield f"data: {initial_event}\n\n"

        try:
            while True:
                # Wait for next event with a periodic heartbeat
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # Heartbeat comment to keep SSE connection alive
                    yield ": ping\n\n"
        except asyncio.CancelledError:
            swarm_state.unsubscribe(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
