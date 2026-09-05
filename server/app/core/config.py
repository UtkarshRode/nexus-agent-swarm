import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Optional Live LLM API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Default LLM Provider: 'gemini', 'openai', 'groq', or 'simulation'
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "simulation")

    # Sandboxed workspace directory for generated files
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    WORKSPACE_DIR: Path = BASE_DIR / "workspace_sandbox"

    # Execution limits
    SANDBOX_TIMEOUT_SECONDS: int = int(os.getenv("SANDBOX_TIMEOUT_SECONDS", "15"))
    MAX_SELF_CORRECTION_LOOPS: int = 3
    REQUIRE_HUMAN_APPROVAL_FOR_DESTRUCTIVE: bool = os.getenv("REQUIRE_HUMAN_APPROVAL_FOR_DESTRUCTIVE", "true").lower() == "true"

settings = Settings()

# Ensure workspace sandbox exists
settings.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
