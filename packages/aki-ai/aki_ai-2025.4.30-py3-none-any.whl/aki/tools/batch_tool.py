"""Batch Tool for parallel execution of multiple tools in a single request."""

import asyncio
import logging
from typing import Dict, List, Any, ClassVar
from pydantic import BaseModel, Field, ConfigDict

from langchain.tools import BaseTool

from aki.tools.param_conversion import (
    convert_tool_args,
    identify_tools_needing_conversion,
)


class ToolInvocation(BaseModel):
    """Model for a single tool invocation within the batch."""

    name: str = Field(description="Name of the tool to invoke")
    parameters: Dict[str, Any] = Field(description="Parameters to pass to the tool")


class BatchToolInput(BaseModel):
    """Input schema for the BatchTool."""

    invocations: List[ToolInvocation] = Field(
        description="List of tool invocations to execute in parallel"
    )


class BatchTool(BaseTool):
    """Tool for executing multiple tool calls in parallel.

    This tool allows the model to make multiple tool calls simultaneously,
    improving response time for operations that would otherwise require
    multiple back-and-forth interactions.
    """

    name: str = "batch_tool"
    description: str = """
    Execute multiple tool calls simultaneously to reduce latency.
    
    WHEN TO USE:
    - Combining 2+ tools in a single operation (file reads + code analysis)
    - Fetching multiple pieces of information simultaneously (multiple file reads)
    - Running analysis tools alongside tasklist / think tool for complex reasoning
    
    WHEN NOT TO USE:
    - Single tool operations (use direct tool calls instead)
    - Sequential operations with dependencies
    - When the results of one operation determine the next steps
    
    Each invocation must include:
    1. The 'name' of the tool to call
    2. The 'parameters' as a dictionary matching that tool's schema
    
    Example (RECOMMENDED):
    ```json
    {
      "invocations": [
        {
          "name": "read_file",
          "parameters": {"file_path": "config.json"}
        },
        {
          "name": "think",
          "parameters": {"thought": "Analyzing config structure..."}
        },
        {
          "name": "file_search",
          "parameters": {"pattern": "*.py", "dir_path": "src"}
        }
      ]
    }
    ```
    """

    args_schema: ClassVar[type[BaseModel]] = BatchToolInput

    # This attribute tells the parameter converter to process the tool
    needs_param_conversion: bool = True

    # Configure model with extra fields allowed
    model_config = ConfigDict(extra="allow")

    def __init__(
        self, tools_dict: Dict[str, BaseTool], *args: Any, **kwargs: Any
    ) -> None:
        """Initialize with available tools dictionary.

        Args:
            tools_dict: Dictionary mapping tool names to tool instances
        """
        super().__init__(*args, **kwargs)
        self._tools_dict = tools_dict  # Store as a private attribute
        # Identify tools needing parameter conversion
        self._tools_with_param_conversion = identify_tools_needing_conversion(
            list(tools_dict.values())
        )

        logging.debug(f"BatchTool initialized with {len(tools_dict)} available tools")

    async def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a single tool asynchronously.

        Args:
            tool_name: Name of the tool to invoke
            parameters: Dictionary of parameters to pass to the tool

        Returns:
            Tool execution result or error message
        """
        if tool_name not in self._tools_dict:
            return {"error": f"Tool '{tool_name}' not found"}

        try:
            # Get the tool
            tool = self._tools_dict[tool_name]

            # Apply parameter conversion if needed
            if tool_name in self._tools_with_param_conversion:
                parameters = convert_tool_args(
                    tool_name, parameters, self._tools_with_param_conversion
                )

            # Execute the tool
            if hasattr(tool, "_arun"):
                result = await tool._arun(**parameters)
            else:
                # Fall back to sync execution for tools without async support
                result = tool._run(**parameters)

            return result
        except Exception as e:
            logging.debug(f"Error executing {tool_name}: {str(e)}", exc_info=True)
            return {"error": f"Tool execution failed: {str(e)}"}

    async def _arun(self, invocations: List[ToolInvocation]) -> str:
        """Execute multiple tool calls in parallel.

        Args:
            invocations: List of tool invocations

        Returns:
            Dictionary with results from all tools
        """
        if not invocations:
            return "No tool invocations provided"

        # Create tasks for all tool invocations
        tasks = []
        for inv in invocations:
            tasks.append(self._execute_tool(inv.name, inv.parameters))

        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks)

        # Format results to match the expected content block format
        formatted_results = {}
        tool_counts = {}

        for i, result in enumerate(results):
            tool_name = invocations[i].name

            # Track the number of times this tool has been used
            if tool_name in tool_counts:
                tool_counts[tool_name] += 1
                key = f"{tool_name}_{tool_counts[tool_name]}"
            else:
                tool_counts[tool_name] = 0
                key = tool_name

            # Store result with the appropriate key
            formatted_results[key] = result

        # Return as a recognized content block that will be properly rendered by Chainlit
        return [{"type": "json", "json": formatted_results}]

    def _run(self, invocations: List[ToolInvocation]) -> str:
        """Synchronous execution is not supported."""
        raise NotImplementedError(
            "BatchTool only supports async execution. Use _arun instead."
        )


def create_batch_tool(tools_dict: Dict[str, BaseTool]) -> BatchTool:
    """Create a BatchTool instance with the provided tools dictionary.

    Args:
        tools_dict: Dictionary mapping tool names to tool instances

    Returns:
        BatchTool instance
    """
    return BatchTool(tools_dict=tools_dict)
