import uvicorn
import os
from app.core.config import settings

if __name__ == "__main__":
    print("====================================================")
    print("🤖 NEXUS-SWARM: MULTI-AGENT ORCHESTRATION BACKEND")
    print(f"📡 API Server: http://localhost:{settings.PORT}")
    print(f"⚡ Docs: http://localhost:{settings.PORT}/docs")
    print("====================================================")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
