from pathlib import Path
from app.core.config import settings
from app.core.state import swarm_state
from app.tools.registry import tool_registry

@tool_registry.register(
    name="write_file",
    description="Writes source code or text to a file in the sandboxed workspace. Updates the artifact viewer.",
    parameters_schema={
        "type": "object",
        "properties": {
            "filename": {"type": "string", "description": "The name of the file to write (e.g. solution.py, test_solution.py)"},
            "content": {"type": "string", "description": "The exact source code or content to write into the file"},
            "language": {"type": "string", "description": "Programming language identifier (python, javascript, markdown)", "default": "python"}
        },
        "required": ["filename", "content"]
    },
    requires_approval=False
)
async def write_file(filename: str, content: str, language: str = "python") -> str:
    target_path = settings.WORKSPACE_DIR / filename
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    
    # Register artifact in swarm state
    await swarm_state.save_artifact(filename, content, language)
    return f"Successfully wrote {len(content)} characters to '{filename}'."

@tool_registry.register(
    name="read_file",
    description="Reads the content of an existing file from the sandboxed workspace.",
    parameters_schema={
        "type": "object",
        "properties": {
            "filename": {"type": "string", "description": "Name of the file to read"}
        },
        "required": ["filename"]
    }
)
def read_file(filename: str) -> str:
    target_path = settings.WORKSPACE_DIR / filename
    if not target_path.exists():
        return f"Error: File '{filename}' not found."
    return target_path.read_text(encoding="utf-8")

@tool_registry.register(
    name="list_directory",
    description="Lists all files currently present in the sandboxed workspace.",
    parameters_schema={
        "type": "object",
        "properties": {}
    }
)
def list_directory() -> str:
    files = [f.name for f in settings.WORKSPACE_DIR.iterdir() if f.is_file()]
    if not files:
        return "Workspace is empty. No files created yet."
    return "Files in workspace:\n" + "\n".join(f"- {f}" for f in files)
