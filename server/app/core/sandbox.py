import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.config import settings

class ExecutionResult:
    def __init__(
        self,
        stdout: str,
        stderr: str,
        return_code: int,
        execution_time_ms: float,
        timeout_occurred: bool = False
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code
        self.execution_time_ms = execution_time_ms
        self.timeout_occurred = timeout_occurred
        self.success = (return_code == 0 and not timeout_occurred)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "timeout_occurred": self.timeout_occurred,
            "success": self.success,
        }

class PythonSandbox:
    @staticmethod
    def execute_code(code_str: str, filename: str = "temp_runner.py") -> ExecutionResult:
        file_path = settings.WORKSPACE_DIR / filename
        file_path.write_text(code_str, encoding="utf-8")
        return PythonSandbox.execute_file(file_path)

    @staticmethod
    def execute_file(file_path: Path) -> ExecutionResult:
        if not file_path.exists():
            return ExecutionResult(
                stdout="",
                stderr=f"Error: File '{file_path.name}' does not exist.",
                return_code=-1,
                execution_time_ms=0,
            )

        start_time = time.perf_counter()
        try:
            # Run using the current python interpreter
            process = subprocess.run(
                [sys.executable, str(file_path.resolve())],
                cwd=str(settings.WORKSPACE_DIR),
                capture_output=True,
                text=True,
                timeout=settings.SANDBOX_TIMEOUT_SECONDS,
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                stdout=process.stdout,
                stderr=process.stderr,
                return_code=process.returncode,
                execution_time_ms=elapsed_ms,
            )
        except subprocess.TimeoutExpired:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                stdout="",
                stderr=f"Execution timed out after {settings.SANDBOX_TIMEOUT_SECONDS} seconds.",
                return_code=-2,
                execution_time_ms=elapsed_ms,
                timeout_occurred=True,
            )
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                stdout="",
                stderr=f"Execution error: {str(e)}",
                return_code=-3,
                execution_time_ms=elapsed_ms,
            )

sandbox = PythonSandbox()
