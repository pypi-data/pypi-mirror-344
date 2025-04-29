import chainlit as cl
from langchain_core.tools import BaseTool, ToolException
from typing import Dict, Any
from pydantic import BaseModel, Field
import asyncio

# Global dictionary to store rendering status
mermaid_render_status = {}


# Window message handler for Mermaid rendering status
@cl.on_window_message
async def on_mermaid_status(data: Dict[str, Any]):
    """Handle status messages from the Mermaid renderer."""
    if data.get("type") != "mermaid-render-status":
        return

    # Store the status in the global dictionary
    diagram_id = data.get("diagramId")
    status = data.get("status")
    error = data.get("error", "")

    # Store the status using the diagram ID as key
    key = diagram_id or "latest"
    mermaid_render_status[key] = {
        "status": status,
        "success": status == "success",
        "error": error,
    }

    # Always update the 'latest' key too for easy access
    if key != "latest":
        mermaid_render_status["latest"] = {
            "status": status,
            "success": status == "success",
            "error": error,
        }


class RenderMermaidInput(BaseModel):
    """Input for rendering Mermaid diagram content."""

    mermaid_code: str = Field(description="Mermaid diagram code to render")


# Define the on_element_update function to handle diagram updates
async def on_element_update(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle updates to the Mermaid diagram element."""
    # Return the updated mermaid code
    return {"mermaidCode": event.get("value", "")}


class RenderMermaidTool(BaseTool):
    """Tool for rendering Mermaid diagrams using a custom renderer."""

    name: str = "render_mermaid"
    description: str = """Renders Mermaid diagram code in the chat UI.
    This tool takes mermaid code as input and renders a pretty diagram with zoom and popup capabilities.
    Use this when you want to visualize diagrams like flowcharts, sequence diagrams, gantt charts, etc.
    If the mermaid code is invalid, the tool will output the syntax error message.
    
    When using this tool, DO NOT include the raw Mermaid code in your text response,
    as the diagram will be rendered directly by the tool. Duplicating the code is unnecessary
    and creates a poor user experience.
    """
    args_schema: type[BaseModel] = RenderMermaidInput

    async def _arun(self, mermaid_code: str) -> str:
        """Run the tool asynchronously."""
        try:
            if not mermaid_code:
                raise ValueError("Mermaid code must be provided")

            # Clear any previous status
            mermaid_render_status.clear()

            # Create the element but don't send it yet
            element = cl.CustomElement(
                name="MermaidRenderer",
                props={"mermaidCode": mermaid_code},
                display="inline",
                on_update=on_element_update,
            )

            # Create a temporary message to trigger validation
            temp_msg = cl.Message(content="", elements=[element])
            await temp_msg.send()

            # Wait briefly for errors (errors usually come back quickly)
            await asyncio.sleep(0.5)

            # Check if we have an error status
            for key, status_info in mermaid_render_status.items():
                if (
                    isinstance(status_info, dict)
                    and status_info.get("status") == "error"
                ):
                    # Found an error, remove the temp message
                    await temp_msg.remove()

                    error_message = status_info.get("error", "Unknown rendering error")
                    raise ToolException(
                        f"Mermaid diagram rendering failed: {error_message}"
                    )

            # No error detected, keep the message and return success
            return "Mermaid diagram rendered successfully"

        except Exception as e:
            raise ToolException(str(e))

    def _run(self, mermaid_code: str) -> str:
        """Synchronous wrapper for _arun."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._arun(mermaid_code))


def create_render_mermaid_tool() -> RenderMermaidTool:
    """Create and return a RenderMermaidTool instance."""
    return RenderMermaidTool()
