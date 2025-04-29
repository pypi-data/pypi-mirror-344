import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from aki.tools.code_executor import create_execute_python_tool

# Import directly from the module
from aki.tools.code_executor import (
    ExecutePythonTool,
    ExecutePythonInput,
    SecurityChecker,
    CodeExecutionTimeoutError,
    CodeValidationError,
    CodeExecutionConfig,
    SAFE_MODULES,
)


#####################################################
# Fixtures
#####################################################


@pytest.fixture
def executor_tool():
    """Create an ExecutePythonTool with mocked dependencies."""
    # Mock chainlit if it's imported in the tool
    with patch("aki.tools.code_executor.chainlit", create=True) as mock_cl:
        # Set up mock state with workspace_dir
        mock_state = {"workspace_dir": os.getcwd()}
        mock_cl.user_session.get.return_value = mock_state

        # Create and return the tool
        tool = create_execute_python_tool()
        return tool


#####################################################
# Configuration Tests
#####################################################


def test_default_config():
    """Verify that CodeExecutionConfig default values match our expectations."""
    config = CodeExecutionConfig()
    assert config.MAX_CODE_SIZE == 10000, "MAX_CODE_SIZE should be 10000"


def test_config_initialization(executor_tool):
    """Ensure that ExecutePythonTool properly initializes with config and security checker."""
    assert executor_tool.config is not None, "Tool should have a config"
    assert isinstance(
        executor_tool.config, CodeExecutionConfig
    ), "Config should be a CodeExecutionConfig"
    assert (
        executor_tool.security_checker is not None
    ), "Tool should have a security checker"
    assert isinstance(
        executor_tool.security_checker, SecurityChecker
    ), "Security checker should be a SecurityChecker"


#####################################################
# Input Validation Tests
#####################################################


def test_validate_code_syntax_valid():
    """Test that valid Python code passes validation."""
    valid_code = "print('Hello, World!')"
    # This should not raise any exception
    validated = ExecutePythonInput.validate_code_syntax(valid_code)
    assert validated == valid_code


def test_validate_code_syntax_invalid():
    """Test that invalid Python code fails validation."""
    invalid_code = "print('Unclosed string"
    with pytest.raises(CodeValidationError) as excinfo:
        ExecutePythonInput.validate_code_syntax(invalid_code)
    assert "Syntax error" in str(excinfo.value)


def test_validate_code_syntax_empty():
    """Test that empty code fails validation."""
    with pytest.raises(CodeValidationError) as excinfo:
        ExecutePythonInput.validate_code_syntax("")
    assert "Code cannot be empty" in str(excinfo.value)

    with pytest.raises(CodeValidationError) as excinfo:
        ExecutePythonInput.validate_code_syntax("  \n  ")
    assert "Code cannot be empty" in str(excinfo.value)


def test_validate_code_size_limit():
    """Test that code exceeding MAX_CODE_SIZE fails validation."""
    max_size = CodeExecutionConfig.MAX_CODE_SIZE
    large_code = "x = 1\n" * (max_size // 5 + 1)  # Make it slightly larger than allowed

    with pytest.raises(CodeValidationError) as excinfo:
        ExecutePythonInput.validate_code_syntax(large_code)
    assert "exceeds maximum length" in str(excinfo.value)


#####################################################
# SecurityChecker Tests
#####################################################


def test_security_checker_safe_code():
    """Test that safe code has no violations."""
    checker = SecurityChecker()
    safe_code = "import math\nprint(math.pi)"
    violations = checker.check_code(safe_code)
    assert len(violations) == 0, "Safe code should have no violations"


def test_security_checker_restricted_direct_import():
    """Test detection of restricted direct imports."""
    checker = SecurityChecker()
    unsafe_code = "import subprocess\nsubprocess.run(['ls'])"
    violations = checker.check_code(unsafe_code)
    assert len(violations) > 0, "Should detect restricted module"
    assert any(
        "subprocess" in v for v in violations
    ), "Should specifically mention 'subprocess'"


def test_security_checker_restricted_from_import():
    """Test detection of restricted from imports."""
    checker = SecurityChecker()
    unsafe_code = "from os import system\nsystem('ls')"
    violations = checker.check_code(unsafe_code)
    assert len(violations) > 0
    assert any("os" in v for v in violations)


def test_security_checker_mixed_imports():
    """Test code with both safe and restricted imports."""
    checker = SecurityChecker()
    mixed_code = "import math\nimport subprocess\nimport json"
    violations = checker.check_code(mixed_code)
    assert len(violations) == 1, "Should detect exactly one restricted module"
    assert any(
        "subprocess" in v for v in violations
    ), "Should specifically mention 'subprocess'"


def test_execution_timeout(executor_tool):
    """Test that execution times out for infinite loops."""
    # Create a side effect that raises a timeout exception when _execute_with_timeout is called
    with patch.object(executor_tool, "_execute_with_timeout") as mock_execute:
        mock_execute.side_effect = CodeExecutionTimeoutError(
            f"Code execution timed out after {executor_tool.timeout} seconds"
        )

        # Create a mock for chainlit to intercept direct imports
        mock_chainlit = MagicMock()
        mock_state = {"workspace_dir": os.getcwd()}
        mock_chainlit.user_session.get.return_value = mock_state

        # Mock at sys.modules level to intercept the direct import
        with patch.dict("sys.modules", {"chainlit": mock_chainlit}):
            with (
                patch("aki.tools.code_executor.io.StringIO"),
                patch("aki.tools.code_executor.contextlib.redirect_stdout"),
                patch("aki.tools.code_executor.contextlib.redirect_stderr"),
            ):
                # Run code that would cause an infinite loop
                result = executor_tool._run("while True: pass")

                # Check that timeout is reported
                assert "timeout" in result.lower()
                assert (
                    str(executor_tool.timeout) in result
                ), "Should include the timeout value"


#####################################################
# Execution Tests
#####################################################


def test_successful_execution(executor_tool):
    """Test successful code execution with output capture."""
    # Create a mock for chainlit to intercept direct imports
    mock_chainlit = MagicMock()
    mock_state = {"workspace_dir": os.getcwd()}
    mock_chainlit.user_session.get.return_value = mock_state

    # Mock at sys.modules level to intercept the direct import
    with patch.dict("sys.modules", {"chainlit": mock_chainlit}):
        # Mock internal components to avoid actual execution
        with (
            patch("aki.tools.code_executor.io.StringIO") as mock_stringio,
            patch("aki.tools.code_executor.contextlib.redirect_stdout"),
            patch("aki.tools.code_executor.contextlib.redirect_stderr"),
            patch.object(executor_tool, "_execute_with_timeout"),
        ):
            # Set up our mock StringIO to return specific content
            mock_stdout = MagicMock()
            mock_stderr = MagicMock()
            mock_log = MagicMock()
            mock_stdout.getvalue.return_value = "Hello, World!"
            mock_stderr.getvalue.return_value = ""
            mock_log.getvalue.return_value = ""

            # Mock StringIO to return our mocks
            mock_stringio.side_effect = [mock_stdout, mock_stderr, mock_log]

            # Run the code
            code = "print('Hello, World!')"
            result = executor_tool._run(code)

            # Check result
            assert "Hello, World!" in result


def test_execution_with_error(executor_tool):
    """Test code execution with runtime error."""
    # Create an ExecutionResult with an error
    from aki.tools.code_executor import ExecutionResult

    error_result = ExecutionResult()
    error_result.error = ZeroDivisionError("division by zero")

    # Create a mock for chainlit to intercept direct imports
    mock_chainlit = MagicMock()
    mock_state = {"workspace_dir": os.getcwd()}
    mock_chainlit.user_session.get.return_value = mock_state

    # Mock at sys.modules level to intercept the direct import
    with patch.dict("sys.modules", {"chainlit": mock_chainlit}):
        # Mock to simulate an execution error
        with patch.object(executor_tool, "_execute_with_timeout") as mock_execute:
            mock_execute.return_value = error_result

            with (
                patch("aki.tools.code_executor.io.StringIO") as mock_stringio,
                patch("aki.tools.code_executor.contextlib.redirect_stdout"),
                patch("aki.tools.code_executor.contextlib.redirect_stderr"),
            ):
                # Set up our mock StringIO to return specific content
                mock_stdout = MagicMock()
                mock_stderr = MagicMock()
                mock_log = MagicMock()
                mock_stdout.getvalue.return_value = ""
                mock_stderr.getvalue.return_value = ""
                mock_log.getvalue.return_value = ""

                # Mock StringIO to return our mocks
                mock_stringio.side_effect = [mock_stdout, mock_stderr, mock_log]

                code = "1/0"
                result = executor_tool._run(code)

                # Check for error indication
                assert any(
                    term in result.lower()
                    for term in ["error", "exception", "division by zero"]
                )


def test_stdout_stderr_capture(executor_tool):
    """Test that stdout and stderr are properly captured."""
    tool = ExecutePythonTool()
    with tool._capture_output() as (stdout, stderr, _):
        print("Test stdout")
        print("Test stderr", file=sys.stderr)

    assert "Test stdout" in stdout.getvalue()
    assert "Test stderr" in stderr.getvalue()


#####################################################
# Security Enforcement Tests
#####################################################


def test_restricted_module_import_blocked(executor_tool):
    """Test that importing restricted modules is blocked."""
    code = "import subprocess; subprocess.run(['ls'])"

    # Create a mock for chainlit to intercept direct imports
    mock_chainlit = MagicMock()
    mock_state = {"workspace_dir": os.getcwd()}
    mock_chainlit.user_session.get.return_value = mock_state

    # Mock at sys.modules level to intercept the direct import
    with patch.dict("sys.modules", {"chainlit": mock_chainlit}):
        # No need to mock execution since security check should happen before execution
        with (
            patch("aki.tools.code_executor.io.StringIO"),
            patch("aki.tools.code_executor.contextlib.redirect_stdout"),
            patch("aki.tools.code_executor.contextlib.redirect_stderr"),
        ):
            with patch("subprocess.run") as mock_run:
                result = executor_tool._run(code)

            # Check for security violation indication
            assert "Security" in result or "security" in result.lower()
            assert (
                "subprocess" in result
            ), "Should mention the specific restricted module"
            mock_run.assert_not_called()


#####################################################
# Helper Method Tests
#####################################################


def test_prepare_namespace(executor_tool):
    """Test that the namespace has only safe modules."""
    namespace = executor_tool._prepare_namespace()

    # Check that __name__ is set
    assert namespace["__name__"] == "__main__"

    # Check that safe modules are included
    for module_name in SAFE_MODULES:
        if "." not in module_name:
            # Skip modules that might not be available in test environment
            if module_name not in sys.modules and module_name not in ["dateutil"]:
                continue
            assert (
                module_name in namespace or module_name in sys.modules
            ), f"Safe module {module_name} should be in namespace or sys.modules"


def test_format_output(executor_tool):
    """Test that output formatting works correctly."""
    from aki.tools.code_executor import ExecutionResult

    # Create test data
    stdout = "This is stdout"
    stderr = "This is stderr"
    logs = "Log entry 1\nGetting data layer None\nLog entry 2"
    result = ExecutionResult()

    # Call the format function
    formatted = executor_tool._format_output(stdout, stderr, logs, result)

    # Check that all expected sections are present
    assert "Output:" in formatted
    assert "This is stdout" in formatted
    assert "Stderr:" in formatted
    assert "This is stderr" in formatted
    assert "Logs:" in formatted
    assert "Log entry 1" in formatted
    assert "Log entry 2" in formatted

    # Check that filtered log line is not present
    assert "Getting data layer None" not in formatted


#####################################################
# Async Method Tests
#####################################################


@pytest.mark.asyncio
async def test_arun_method():
    """Test the asynchronous _arun method."""
    # Create a tool instance
    tool = ExecutePythonTool()

    # Mock the _run method to avoid actual execution
    with patch.object(ExecutePythonTool, "_run") as mock_run:
        mock_run.return_value = "Expected result"

        # Call the async method
        result = await tool._arun("print('test')")

        # Verify it called _run with the right parameters
        assert result == "Expected result"
        mock_run.assert_called_once_with(code="print('test')", run_manager=None)
