from pathlib import Path
from app.core.config import settings
from app.core.sandbox import sandbox
from app.tools.registry import tool_registry

@tool_registry.register(
    name="execute_python",
    description="Executes a Python file in the isolated sandbox. Returns stdout, stderr, and execution time.",
    parameters_schema={
        "type": "object",
        "properties": {
            "filename": {"type": "string", "description": "The Python file to execute inside workspace (e.g. main.py)"}
        },
        "required": ["filename"]
    },
    requires_approval=False
)
def execute_python(filename: str) -> str:
    target_path = settings.WORKSPACE_DIR / filename
    result = sandbox.execute_file(target_path)

    output = []
    output.append(f"Exit Code: {result.return_code} ({'SUCCESS' if result.success else 'FAILED'})")
    output.append(f"Execution Time: {result.execution_time_ms} ms")
    
    if result.stdout:
        output.append(f"\n--- STDOUT ---\n{result.stdout.strip()}")
    if result.stderr:
        output.append(f"\n--- STDERR ---\n{result.stderr.strip()}")
    if not result.stdout and not result.stderr:
        output.append("\n(No output produced)")

    return "\n".join(output)

@tool_registry.register(
    name="run_tests",
    description="Runs automated unit tests for a specific test file using the Python test runner.",
    parameters_schema={
        "type": "object",
        "properties": {
            "test_filename": {"type": "string", "description": "The test script to execute (e.g. test_cache.py)"}
        },
        "required": ["test_filename"]
    }
)
def run_tests(test_filename: str) -> str:
    target_path = settings.WORKSPACE_DIR / test_filename
    result = sandbox.execute_file(target_path)
    
    status_str = "PASSED" if result.success else "FAILED / ERRORS ENCOUNTERED"
    return f"Test Execution {status_str}\n{result.stdout}\n{result.stderr}"
