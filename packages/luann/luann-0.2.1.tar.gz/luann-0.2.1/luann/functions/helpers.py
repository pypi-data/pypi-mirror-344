from typing import Any, Optional, Union
import json
from pydantic import BaseModel
from luann.schemas.enums import MessageRole
from luann.schemas.luann_message import AssistantMessage, ReasoningMessage, ToolCallMessage
from luann.schemas.luann_response import LuannResponse
from luann.schemas.message import MessageCreate
from luann.constants import  DEFAULT_MESSAGE_TOOL, DEFAULT_MESSAGE_TOOL_KWARG



def parse_luann_response_for_assistant_message(
    luann_response: LuannResponse,
    assistant_message_tool_name: str = DEFAULT_MESSAGE_TOOL,
    assistant_message_tool_kwarg: str = DEFAULT_MESSAGE_TOOL_KWARG,
) -> Optional[str]:
    reasoning_message = ""
    for m in luann_response.messages:
        if isinstance(m, AssistantMessage):
            return m.assistant_message
        elif isinstance(m, ToolCallMessage) and m.tool_call.name == assistant_message_tool_name:
            try:
                return json.loads(m.tool_call.arguments)[assistant_message_tool_kwarg]
            except Exception:  # TODO: Make this more specific
                continue
        elif isinstance(m, ReasoningMessage):
            # This is not ideal, but we would like to return something rather than nothing
            reasoning_message += f"{m.reasoning}\n"

    return None

import asyncio
from random import uniform
from typing import Optional
async def async_send_message_with_retries(
    server,
    sender_agent: "Agent",
    target_agent_id: str,
    message_text: str,
    max_retries: int,
    timeout: int,
    logging_prefix: Optional[str] = None,
) -> str:
    """
    Shared helper coroutine to send a message to an agent with retries and a timeout.

    Args:
        server: The luann server instance (from luann.get_luann_server()).
        sender_agent (Agent): The agent initiating the send action.
        target_agent_id (str): The ID of the agent to send the message to.
        message_text (str): The text to send as the user message.
        max_retries (int): Maximum number of retries for the request.
        timeout (int): Maximum time to wait for a response (in seconds).
        logging_prefix (str): A prefix to append to logging
    Returns:
        str: The response or an error message.
    """
    logging_prefix = logging_prefix or "[async_send_message_with_retries]"
    for attempt in range(1, max_retries + 1):
        try:
            messages = [MessageCreate(role=MessageRole.user, text=message_text, name=sender_agent.agent_state.name)]
            # Wrap in a timeout
            response = await asyncio.wait_for(
                server.send_message_to_agent(
                    agent_id=target_agent_id,
                    actor=sender_agent.user,
                    messages=messages,
                    stream_steps=False,
                    stream_tokens=False,
                    use_assistant_message=True,
                    assistant_message_tool_name=DEFAULT_MESSAGE_TOOL,
                    assistant_message_tool_kwarg=DEFAULT_MESSAGE_TOOL_KWARG,
                ),
                timeout=timeout,
            )

            # Extract assistant message
            assistant_message = parse_luann_response_for_assistant_message(
                response,
                assistant_message_tool_name=DEFAULT_MESSAGE_TOOL,
                assistant_message_tool_kwarg=DEFAULT_MESSAGE_TOOL_KWARG,
            )
            if assistant_message:
                msg = f"Agent {target_agent_id} said '{assistant_message}'"
                sender_agent.logger.info(f"{logging_prefix} - {msg}")
                return msg
            else:
                msg = f"(No response from luann.agent {target_agent_id})"
                sender_agent.logger.info(f"{logging_prefix} - {msg}")
                return msg
        except asyncio.TimeoutError:
            error_msg = f"(Timeout on attempt {attempt}/{max_retries} for agent {target_agent_id})"
            sender_agent.logger.warning(f"{logging_prefix} - {error_msg}")
        except Exception as e:
            error_msg = f"(Error on attempt {attempt}/{max_retries} for agent {target_agent_id}: {e})"
            sender_agent.logger.warning(f"{logging_prefix} - {error_msg}")

        # Exponential backoff before retrying
        if attempt < max_retries:
            backoff = uniform(0.5, 2) * (2**attempt)
            sender_agent.logger.warning(f"{logging_prefix} - Retrying the agent to agent send_message...sleeping for {backoff}")
            await asyncio.sleep(backoff)
        else:
            sender_agent.logger.error(f"{logging_prefix} - Fatal error during agent to agent send_message: {error_msg}")
            return error_msg
