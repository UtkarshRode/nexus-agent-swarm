from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title="NexusSwarm Autonomous AI Agent Engine",
    description="Autonomous Multi-Agent Research & Code Analysis Swarm with ReAct loops and sandboxed execution",
    version="1.0.0",
)

# CORS middleware for local Vite and cloud frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "NexusSwarm Autonomous Multi-Agent Engine",
        "status": "ONLINE",
        "version": "1.0.0",
        "documentation": "https://github.com/UtkarshRode/nexus-agent-swarm",
        "endpoints": {
            "health": "/api/health",
            "execute": "/api/swarm/execute",
            "stream": "/api/swarm/stream",
            "status": "/api/swarm/status",
        },
    }

# Mount API routes
app.use_route_names_as_operation_ids = True
app.include_router(api_router)
