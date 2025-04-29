"""Code execution tools with enhanced security and validation"""

import ast
import io
import os
import logging
import contextlib
import traceback
import concurrent
from typing import Optional, Type, Dict, Any, Set, List, Final
from dataclasses import dataclass, field
from logging import StreamHandler, getLogger
from pydantic import Field


from pydantic import BaseModel, field_validator
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun

logger = logging.getLogger(__name__)


@dataclass
class CodeExecutionConfig:
    """Configuration settings for code execution."""

    MAX_CODE_SIZE: Final[int] = 10000  # Maximum code length in characters


# List of modules that are considered risky
RESTRICTED_MODULES: Set[str] = {
    # could be vulnerable with user input injection and comprise the system
    "subprocess",
    # could be risky with user input injection and execute shell command directly
    "os.system",
    # could delete / modify files
    "shutil",
    # could establish unauthorized connection
    "socket",
    # could leak internal data
    "requests",
    # could make outbound connection (to malicious endpoint etc)
    "urllib",
    # could expose to FTP attacks
    "ftplib",
    # could expose to insecure protocol
    "telnetlib",
    # could send unauthorized email
    "smtplib",
    # could execute arbitrate code
    "pickle",
    # could spawn unwanted processes
    "multiprocessing",
    # could read/write arbitrate memory or make system call
    "ctypes",
    # could load restricted modules
    "importlib",
}


# Safe modules that are always allowed
SAFE_MODULES: Set[str] = {
    "math",
    "random",
    "datetime",
    "collections",
    "itertools",
    "functools",
    "string",
    "re",
    "json",
    "copy",
    "typing",
}


@dataclass
class ExecutionResult:
    completed: bool = False
    output: str = ""
    error: Optional[Exception] = None


class CodeValidationError(Exception):
    """Raised when code validation fails."""

    pass


class CodeExecutionTimeoutError(Exception):
    """Exception raised when code execution exceeds the maximum allowed time."""

    pass


@dataclass
class SecurityChecker:
    """AST visitor that checks for restricted module imports."""

    violations: Set[str] = field(default_factory=set)

    def check_code(self, code: str) -> List[str]:
        self.violations.clear()
        try:
            tree = ast.parse(code)
            self.check_imports(tree)
            self.check_importFrom(tree)
            return self.violations
        except SyntaxError:
            self.violations.append("Contains incorrect syntax in the Python code")
            return self.violations

    def check_imports(self, tree: ast.AST) -> None:
        """Check for restricted modules in import statements."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    if name.name in RESTRICTED_MODULES:
                        self._add_violation(name.name)
                    else:
                        for restricted in RESTRICTED_MODULES:
                            # Check if this module is a parent of any restricted functionality
                            # e.g., "import os" when "os.system" is restricted
                            if restricted.startswith(name.name + "."):
                                self._add_violation(
                                    f"{name.name} (gives access to {restricted})"
                                )
                                break

    def check_importFrom(self, tree: ast.AST) -> None:
        """Check for restricted modules in 'from ... import' statements."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module in RESTRICTED_MODULES:
                    self._add_violation(node.module)
                    continue
                if node.module:
                    for name in node.names:
                        # Construct the full name (e.g., "os.system" from "from os import system")
                        full_name = f"{node.module}.{name.name}"
                        if full_name in RESTRICTED_MODULES:
                            self._add_violation(
                                f"{full_name} (imported as {name.name})"
                            )

    def _add_violation(self, module_name: str) -> None:
        """Add a module violation to the violations list."""
        self.violations.add(f"Restricted module: {module_name}")


class ExecutePythonInput(BaseModel):
    """Input schema for ExecutePythonTool."""

    code: str = Field(
        description="Python code to execute",
        max_length=CodeExecutionConfig.MAX_CODE_SIZE,
    )

    @field_validator("code")
    @classmethod
    def validate_code_syntax(cls, input_code: str) -> str:
        """Validate syntax before execution."""
        # Check for empty input
        if not input_code or not input_code.strip():
            raise CodeValidationError("Code cannot be empty")

        # check for max size
        if len(input_code) > CodeExecutionConfig.MAX_CODE_SIZE:
            raise CodeValidationError(
                f"Code exceeds maximum length of {CodeExecutionConfig.MAX_CODE_SIZE} characters"
            )

        try:
            ast.parse(input_code)
            return input_code
        except SyntaxError as e:
            error_msg = f"Syntax error in code: {str(e)}"
            logger.error(error_msg)
            raise CodeValidationError(error_msg) from e
        except Exception as e:
            error_msg = f"Code validation failed: {str(e)}"
            logger.error(error_msg)
            raise CodeValidationError(error_msg) from e


class ExecutePythonTool(BaseTool):
    """Tool for executing Python code with enhanced security and validation."""

    name: str = "execute_python"
    args_schema: Type[BaseModel] = ExecutePythonInput
    description: str = (
        "Execute python code that contains allowed modules "
        '"math","random", "datetime", "collections", "itertools", "functools", "string", "re", "json", "copy", "typing".'
    )
    config: CodeExecutionConfig = Field(default_factory=CodeExecutionConfig)
    security_checker: SecurityChecker = Field(default_factory=SecurityChecker)
    timeout: Optional[int] = None

    def __init__(self):
        """Initialize the tool with configuration and security checker."""
        super().__init__()
        self.config = CodeExecutionConfig()
        self.security_checker = SecurityChecker()
        self.timeout = int(os.getenv("AKI_TOOL_TIME_OUT_THRESHOLD", "60"))

    def _check_security(self, code: str) -> List[str]:
        """Perform security checks on code."""
        # Always initialize before use to ensure it exists
        if not hasattr(self, "security_checker") or self.security_checker is None:
            self.security_checker = SecurityChecker()
        if not hasattr(self, "config") or self.config is None:
            self.config = CodeExecutionConfig()
        return self.security_checker.check_code(code)

    @contextlib.contextmanager
    def _capture_output(self):
        """Context manager for capturing stdout and stderr."""
        stdout = io.StringIO()
        stderr = io.StringIO()
        log_capture = io.StringIO()
        log_handler = StreamHandler(log_capture)
        root_logger = getLogger()

        # Add log handler temporarily
        root_logger.addHandler(log_handler)

        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                yield stdout, stderr, log_capture
        finally:
            root_logger.removeHandler(log_handler)
            # No need to close here as it will be done in _run

    def _execute_with_timeout(
        self, code: str, namespace: Dict[Any, Any]
    ) -> ExecutionResult:
        """Execute code with timeout protection."""
        result = ExecutionResult()

        def target():
            try:
                exec(code, namespace)
                result.completed = True
            except Exception as e:
                result.error = e
            return result

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(target)
            try:
                future.result(timeout=self.timeout)
            except concurrent.futures.TimeoutError:
                # This properly cancels the future when possible
                future.cancel()
                raise CodeExecutionTimeoutError(
                    f"Code execution timed out after {self.config.TIMEOUT} seconds"
                )

        return result

    def _prepare_namespace(self) -> Dict[Any, Any]:
        """Prepare secure execution namespace."""
        namespace = {"__name__": "__main__"}

        # Add safe modules
        for module_name in SAFE_MODULES:
            if "." in module_name:
                parent, child = module_name.split(".", 1)
                parent_mod = __import__(parent, fromlist=[child])
                try:
                    namespace[module_name] = getattr(parent_mod, child)
                except AttributeError:
                    logger.warning(f"Could not import {module_name}")
            else:
                namespace[module_name] = __import__(module_name)

        return namespace

    def _format_output(
        self, stdout: str, stderr: str, logs: str, result: ExecutionResult
    ) -> str:
        """Format execution output."""
        message = ""

        if stdout:
            message += f"Output:\n{stdout}\n"

        if stderr:
            message += f"Stderr:\n{stderr}\n"

        # Filter out irrelevant logs
        relevant_logs = "\n".join(
            line for line in logs.splitlines() if "Getting data layer None" not in line
        )

        if relevant_logs.strip():
            message += f"Logs:\n{relevant_logs}\n"

        if result.error:
            message += f"Exception:\n{str(result.error)}\n"

        return message if message else "Code executed successfully with no output."

    def _run(
        self,
        code: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute Python code securely."""
        logging.debug("Starting code execution")

        try:
            # Get state for workspace_dir (maintaining compatibility with original code)
            state = None
            try:
                import chainlit as cl

                state = cl.user_session.get("state")
                logging.debug(
                    f"Got state with workspace_dir: {state.get('workspace_dir') if state else None}"
                )
            except ImportError:
                logging.warning("Chainlit not available, running without state")

            # Get workspace directory for saving artifacts (maintaining compatibility)
            workspace_dir = (
                state.get("workspace_dir")
                if (state and "workspace_dir" in state)
                else os.getcwd()
            )
            artifacts_dir = os.path.join(workspace_dir, ".artifacts")
            os.makedirs(artifacts_dir, exist_ok=True)

            # 1. Validate input
            try:
                input_model = ExecutePythonInput(code=code)
            except CodeValidationError as e:
                return f"Validation error: {str(e)}"

            # 2. Security checks
            violations = self._check_security(input_model.code)
            if violations:
                return "Security violations found:\n" + "\n".join(violations)

            # 3. Prepare execution environment
            namespace = self._prepare_namespace()

            # 4. Execute with timeout and capture output
            try:
                with self._capture_output() as (stdout, stderr, log_capture):
                    try:
                        result = self._execute_with_timeout(input_model.code, namespace)
                    except CodeExecutionTimeoutError as e:
                        return f"Execution timeout: {str(e)}"

                    return self._format_output(
                        stdout=stdout.getvalue(),
                        stderr=stderr.getvalue(),
                        logs=log_capture.getvalue(),
                        result=result,
                    )
            finally:
                # Make sure to close all StringIO objects
                if "stdout" in locals() and hasattr(stdout, "close"):
                    stdout.close()
                if "stderr" in locals() and hasattr(stderr, "close"):
                    stderr.close()
                if "log_capture" in locals() and hasattr(log_capture, "close"):
                    log_capture.close()

        except Exception as e:
            error_msg = f"Execution failed: {str(e)}\n{traceback.format_exc()}"
            logging.error(error_msg)
            return error_msg

    async def _arun(
        self,
        code: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Async execution wrapper."""
        return self._run(code=code, run_manager=run_manager)


def create_execute_python_tool() -> BaseTool:
    """Create and return the execute python tool."""
    return ExecutePythonTool()


# List of available tools
code_executor_tools = [create_execute_python_tool()]
