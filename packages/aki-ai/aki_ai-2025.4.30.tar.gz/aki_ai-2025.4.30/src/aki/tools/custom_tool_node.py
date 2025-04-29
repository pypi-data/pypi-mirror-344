"""Custom Tool Node implementation with enhanced timeout, response handling, and parameter name conversion."""

import asyncio
import json
import logging
import os
import tiktoken
from typing import Any, Dict, List, Optional, Union, Sequence, Callable
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from aki.config.constants import DEFAULT_MAX_TOOL_TOKENS, DEFAULT_TOKENIZER_MODEL

_tokenizer = tiktoken.get_encoding(DEFAULT_TOKENIZER_MODEL)


def count_tokens(text: str) -> int:
    """Count tokens in text using the configured tokenizer."""
    return len(_tokenizer.encode(text))


def truncate_content(content: Any, max_tokens: int = DEFAULT_MAX_TOOL_TOKENS) -> Any:
    """Truncate content if it exceeds token limit.

    Args:
        content: The content to truncate
        max_tokens: Maximum number of tokens allowed

    Returns:
        Truncated content
    """
    if isinstance(content, str):
        tokens = _tokenizer.encode(content)
        logging.debug(f"Tool response tokens: {len(tokens)}")
        if len(tokens) > max_tokens:
            truncated = _tokenizer.decode(tokens[:max_tokens])
            return truncated + f"\n\n[TRUNCATED: Response exceeded {max_tokens} tokens]"
        return content
    elif isinstance(content, dict):
        return {k: truncate_content(v, max_tokens) for k, v in content.items()}
    elif isinstance(content, list):
        return [truncate_content(item, max_tokens) for item in content]
    return content


def transform_response_format(content: Any) -> Any:
    """
    Transform tool response to unified format.

    This standardizes all tool outputs into a consistent structure regardless of
    the original format, improving consistency for UI rendering and downstream processing.

    Formats:
    - JSON data: [{'type': 'json', 'json': data}]
    - Text content: [{'type': 'text', 'text': text_content}]
    - Image data: [{'type': 'image_url', 'image_url': {'url': image_data_url}}]

    Args:
        content: The original content from a tool response

    Returns:
        Content transformed into the unified format
    """
    # Handle empty list case specifically
    if isinstance(content, list) and len(content) == 0:
        return [{"type": "text", "text": "empty"}]

    # If already in target format, validate its structure
    if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
        try:
            if all(isinstance(item, dict) and "type" in item for item in content):
                types = [item["type"] for item in content if "type" in item]
                if all(t in ["json", "text", "image_url"] for t in types):
                    # Extra validation for json type entries
                    for item in content:
                        if item.get("type") == "json" and "json" in item:
                            # Ensure json field contains valid JSON by serializing and deserializing
                            # This will catch issues with non-serializable objects
                            json_str = json.dumps(item["json"])
                            item["json"] = json.loads(json_str)
                    return content
        except (TypeError, ValueError, json.JSONDecodeError):
            return [{"type": "text", "text": {str(content)}}]

    # Default case - just return as text
    return [{"type": "text", "text": str(content)}]


def process_tool_message(message: ToolMessage) -> ToolMessage:
    """Truncate content in a ToolMessage."""
    if not hasattr(message, "content"):
        return message
    message.content = process_tool_message_content(message.content)
    return message


def process_tool_message_content(content: Any) -> Any:
    """Process tool output with both truncation and transformation.

    This is a convenience function that applies both truncation and transformation
    in the correct order.

    Args:
        output: Raw tool output

    Returns:
        Processed output (truncated and transformed)
    """
    truncated = truncate_content(content)
    transformed = transform_response_format(truncated)
    return transformed


class CustomToolNode(ToolNode):
    """
    Enhanced ToolNode that adds:
    1. Timeout
    2. Response size management
    3. Unified response format for tool outputs

    The unified response format standardizes all tool outputs into a consistent structure:
    - JSON: [{"type": "json", "json": data}]
    - Text: [{"type": "text", "text": content}]
    - Images: [{"type": "image_url", "image_url": {"url": data_url}}]

    Example transformations:

    Before:  "This is a text response"
    After:   [{"type": "text", "text": "This is a text response"}]

    Before:  {"key": "value", "numbers": [1, 2, 3]}
    After:   [{"type": "json", "json": {"key": "value", "numbers": [1, 2, 3]}}]

    Inherits from langgraph's ToolNode to keep the parallel execution benefits.

    Configuration:
    - Timeout: Configurable via AKI_TOOL_TIME_OUT_THRESHOLD environment variable (default: 60 seconds)
    """

    def __init__(
        self,
        tools: Sequence[Union[BaseTool, Callable]],
        *,
        timeout: Optional[int] = None,
        enable_param_conversion: bool = True,
        **kwargs,
    ) -> None:
        """Initialize the custom tool node.

        Args:
            tools: List of tools to be made available
            timeout: Override default timeout from environment
            enable_param_conversion: Whether to automatically convert camelCase to snake_case
                for tool parameters
            **kwargs: Additional arguments passed to ToolNode
        """
        # Initialize parent class first
        super().__init__(tools, **kwargs)

        # Load timeout with precedence:
        # 1. Constructor argument
        # 2. Environment variable
        # 3. Default value (60)
        self.timeout = timeout or int(os.getenv("AKI_TOOL_TIME_OUT_THRESHOLD", "60"))

    async def _arun_one(
        self,
        call: Dict,
        input_type: str,
        config: RunnableConfig,
    ) -> ToolMessage:
        """Run a single tool with parameter name conversion and response transformation."""
        response = await super()._arun_one(call, input_type, config)

        return process_tool_message(response)

    def _run_one(
        self,
        call: Dict,
        input_type: str,
        config: RunnableConfig,
    ) -> ToolMessage:
        """Run a single tool synchronously with parameter conversion and response transformation."""

        # Call the parent implementation
        response = super()._run_one(call, input_type, config)

        return process_tool_message(response)

    async def _afunc(
        self,
        input: Union[List[AIMessage], Dict[str, Any], Any],
        config: RunnableConfig,
        *,
        store: Optional[Any] = None,
    ) -> Any:
        """Enhanced async execution with timeout management."""
        try:
            # Apply timeout to the entire batch of tool executions
            # Note: Individual transformations are now handled in _arun_one and _run_one
            async with asyncio.timeout(self.timeout):
                outputs = await super()._afunc(input, config, store=store)
                return outputs

        except asyncio.TimeoutError:
            # Create timeout response based on input format
            error_msg = f"Tool execution exceeded {self.timeout} seconds timeout"
            logging.warning(error_msg)
            return {"message": error_msg}

        except Exception as e:
            error_msg = f"Error executing tools: {str(e)}"
            logging.error(error_msg, exc_info=True)
            return {"message": error_msg}

    def invoke(self, *args, **kwargs):
        """Synchronous invocation is not supported."""
        raise NotImplementedError(
            "CustomToolNode only supports async invocation. Use ainvoke instead."
        )
