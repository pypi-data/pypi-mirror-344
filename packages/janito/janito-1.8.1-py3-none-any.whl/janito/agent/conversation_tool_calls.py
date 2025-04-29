"""
Helpers for handling tool calls in conversation.
"""

from janito.agent.tool_executor import ToolExecutor
from janito.agent import tool_registry
from .conversation_exceptions import MaxRoundsExceededError
from janito.agent.runtime_config import runtime_config


def handle_tool_calls(tool_calls, message_handler=None):
    max_tools = runtime_config.get("max_tools", None)
    tool_calls_made = 0
    tool_responses = []
    for tool_call in tool_calls:
        if max_tools is not None and tool_calls_made >= max_tools:
            raise MaxRoundsExceededError(
                f"Maximum number of tool calls ({max_tools}) reached in this chat session."
            )
        tool_entry = tool_registry._tool_registry[tool_call.function.name]
        try:
            result = ToolExecutor(message_handler=message_handler).execute(
                tool_entry, tool_call
            )
            tool_responses.append({"tool_call_id": tool_call.id, "content": result})
        except TypeError as e:
            # Return the error as a tool result, asking to retry with correct params
            error_msg = str(e)
            tool_responses.append(
                {
                    "tool_call_id": tool_call.id,
                    "content": f"Tool execution error: {error_msg}. Please retry with the correct parameters.",
                }
            )
        tool_calls_made += 1
    return tool_responses
