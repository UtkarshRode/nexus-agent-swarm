import uvicorn
import os
from app.core.config import settings

if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.PORT))
    host = os.environ.get("HOST", "0.0.0.0")
    is_dev = os.environ.get("ENVIRONMENT", "development") == "development"

    print("====================================================")
    print("🤖 NEXUS-SWARM: MULTI-AGENT ORCHESTRATION BACKEND")
    print(f"📡 API Server: http://{host}:{port}")
    print("====================================================")
    uvicorn.run("app.main:app", host=host, port=port, reload=is_dev)

