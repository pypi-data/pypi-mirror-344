import inspect
import json
import time
import traceback
import warnings
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union
from openai.types.beta.function_tool import FunctionTool as OpenAITool
from luann.constants import (
    CLI_WARNING_PREFIX,
    ERROR_MESSAGE_PREFIX,
    FIRST_MESSAGE_ATTEMPTS,
    FUNC_FAILED_HEARTBEAT_MESSAGE,
    LUANN_CORE_TOOL_MODULE_NAME,
    LUANN_MULTI_AGENT_TOOL_MODULE_NAME,
    LLM_MAX_TOKENS,
    MESSAGE_SUMMARY_WARNING_FRAC,
    REQ_HEARTBEAT_MESSAGE,
)
from luann.errors import ContextWindowExceededError
from luann.functions.functions import get_function_from_module
# from luann.helpers import ToolRulesSolver
from luann.interface import AgentInterface
from luann.llm_api.helpers import calculate_summarizer_cutoff, get_token_counts_for_messages, is_context_overflow_error
from luann.llm_api.llm_api_tools import create
from luann.local_llm.utils import num_tokens_from_functions, num_tokens_from_messages
from luann.log import get_logger
# from luann.memory import summarize_messages
from luann.orm import User
from luann.orm.enums import ToolType
from luann.schemas.agent import AgentState, AgentStepResponse, UpdateAgent
from luann.schemas.block import BlockUpdate
from luann.schemas.embedding_config import EmbeddingConfig
from luann.schemas.enums import MessageRole
from luann.schemas.memory import ContextWindowOverview, Memory
from luann.schemas.message import Message
from luann.schemas.openai.chat_completion_request import Tool as ChatCompletionRequestTool
from luann.schemas.openai.chat_completion_response import ChatCompletionResponse
from luann.schemas.openai.chat_completion_response import Message as ChatCompletionMessage
from luann.schemas.openai.chat_completion_response import UsageStatistics
from luann.schemas.tool import Tool
# from luann.schemas.tool_rule import TerminalToolRule
from luann.schemas.usage import LuannUsageStatistics
from luann.services.agent_manager import AgentManager
from luann.services.block_manager import BlockManager
from luann.services.helpers.agent_manager_helper import compile_memory_metadata_block
from luann.services.job_manager import JobManager
from luann.services.message_manager import MessageManager
from luann.services.passage_manager import PassageManager
from luann.services.provider_manager import ProviderManager
# from luann.services.step_manager import StepManager
from luann.services.tool_execution_sandbox import ToolExecutionSandbox
from luann.services.tool_execution_sandbox import ToolExecutionSandbox
# from luann.settings import summarizer_settings
from luann.streaming_interface import StreamingRefreshCLIInterface
from luann.system import get_heartbeat, get_token_limit_warning, package_function_response, package_summarize_message, package_user_message
from luann.utils import (
    count_tokens,
    get_friendly_error_msg,
    get_tool_call_id,
    get_utc_time,
    json_dumps,
    json_loads,
    parse_json,
    printd,
    validate_function_response,
)
from luann.constants import MESSAGE_SUMMARY_REQUEST_ACK, MESSAGE_SUMMARY_WARNING_FRAC
# from luann.llm_api.llm_api_tools import create
from luann.prompts.gpt_summarize import SYSTEM as SUMMARY_PROMPT_SYSTEM

def _format_summary_history(message_history: List[Message]):
    # TODO use existing prompt formatters for this (eg ChatML)
    return "\n".join([f"{m.role}: {m.text}" for m in message_history])

def summarize_messages(
    agent_state: AgentState,
    message_sequence_to_summarize: List[Message],
):
    """Summarize a message sequence using GPT"""
    # we need the context_window
    context_window = agent_state.llm_config.context_window

    summary_prompt = SUMMARY_PROMPT_SYSTEM
    summary_input = _format_summary_history(message_sequence_to_summarize)
    summary_input_tkns = count_tokens(summary_input)
    if summary_input_tkns > MESSAGE_SUMMARY_WARNING_FRAC * context_window:
        trunc_ratio = (MESSAGE_SUMMARY_WARNING_FRAC * context_window / summary_input_tkns) * 0.8  # For good measure...
        cutoff = int(len(message_sequence_to_summarize) * trunc_ratio)
        summary_input = str(
            [summarize_messages(agent_state, message_sequence_to_summarize=message_sequence_to_summarize[:cutoff])]
            + message_sequence_to_summarize[cutoff:]
        )

    dummy_agent_id = agent_state.id
    message_sequence = []
    message_sequence.append(Message(agent_id=dummy_agent_id, role=MessageRole.system, text=summary_prompt))
    message_sequence.append(Message(agent_id=dummy_agent_id, role=MessageRole.assistant, text=MESSAGE_SUMMARY_REQUEST_ACK))
    message_sequence.append(Message(agent_id=dummy_agent_id, role=MessageRole.user, text=summary_input))

    # TODO: We need to eventually have a separate LLM config for the summarizer LLM
    llm_config_no_inner_thoughts = agent_state.llm_config.model_copy(deep=True)
    llm_config_no_inner_thoughts.put_inner_thoughts_in_kwargs = False
    response = create(
        llm_config=llm_config_no_inner_thoughts,
        user_id=agent_state.created_by_id,
        messages=message_sequence,
        stream=False,
    )

    printd(f"summarize_messages gpt reply: {response.choices[0]}")
    reply = response.choices[0].message.content
    return reply



logger = get_logger(__name__)
class BaseAgent(ABC):
    """
    Abstract class for all agents.
    Only one interface is required: step.
    """

    @abstractmethod
    def step(
        self,
        messages: Union[Message, List[Message]],
    ) -> LuannUsageStatistics:
        """
        Top-level event message handler for the agent.
        """
        raise NotImplementedError


class Agent(BaseAgent):
    def __init__(
        self,
        interface: Optional[Union[AgentInterface, StreamingRefreshCLIInterface]],
        agent_state: AgentState,  # in-memory representation of the agent state (read from luann.multiple tables)
        user: User,
        # extras
        first_message_verify_mono: bool = True,  # TODO move to config?
    ):
        assert isinstance(agent_state.memory, Memory), f"Memory object is not of type Memory: {type(agent_state.memory)}"
        # Hold a copy of the state that was used to init the agent
        self.agent_state = agent_state
        assert isinstance(self.agent_state.memory, Memory), f"Memory object is not of type Memory: {type(self.agent_state.memory)}"

        self.user = user

        # # initialize a tool rules solver
        # if agent_state.tool_rules:
        #     # if there are tool rules, print out a warning
        #     for rule in agent_state.tool_rules:
        #         if not isinstance(rule, TerminalToolRule):
        #             warnings.warn("Tool rules only work reliably for the latest OpenAI models that support structured outputs.")
        #             break
        # # add default rule for having send_message be a terminal tool
        # if agent_state.tool_rules is None:
        #     agent_state.tool_rules = []

        # self.tool_rules_solver = ToolRulesSolver(tool_rules=agent_state.tool_rules)

        # gpt-4, gpt-3.5-turbo, ...
        self.model = self.agent_state.llm_config.model
        # self.supports_structured_output = check_supports_structured_output(model=self.model, tool_rules=agent_state.tool_rules)

        # state managers
        self.block_manager = BlockManager()

        # Interface must implement:
        # - internal_monologue
        # - assistant_message
        # - function_message
        # ...
        # Different interfaces can handle events differently
        # e.g., print in CLI vs send a discord message with a discord bot
        self.interface = interface

        # Create the persistence manager object based on the AgentState info
        self.message_manager = MessageManager()
        self.passage_manager = PassageManager()
        self.provider_manager = ProviderManager()
        self.agent_manager = AgentManager()
        self.job_manager = JobManager()
        # self.step_manager = StepManager()

        # State needed for heartbeat pausing

        self.first_message_verify_mono = first_message_verify_mono

        # Controls if the convo memory pressure warning is triggered
        # When an alert is sent in the message queue, set this to True (to avoid repeat alerts)
        # When the summarizer is run, set this back to False (to reset)
        self.agent_alerted_about_memory_pressure = False

        # Load last function response from luann.message history
        self.last_function_response = self.load_last_function_response()

        # Logger that the Agent specifically can use, will also report the agent_state ID with the logs
        self.logger = get_logger(agent_state.id)

    def load_last_function_response(self):
        """Load the last function response from luann.message history"""
        in_context_messages = self.agent_manager.get_in_context_messages(agent_id=self.agent_state.id, actor=self.user)
        for i in range(len(in_context_messages) - 1, -1, -1):
            msg = in_context_messages[i]
            if msg.role == MessageRole.tool and msg.text:
                try:
                    response_json = json.loads(msg.text)
                    if response_json.get("message"):
                        return response_json["message"]
                except (json.JSONDecodeError, KeyError):
                    raise ValueError(f"Invalid JSON format in message: {msg.text}")
        return None

    def update_memory_if_changed(self, new_memory: Memory) -> bool:
        """
        Update internal memory object and system prompt if there have been modifications.

        Args:
            new_memory (Memory): the new memory object to compare to the current memory object

        Returns:
            modified (bool): whether the memory was updated
        """
        if self.agent_state.memory.compile() != new_memory.compile():
            # update the blocks (LRW) in the DB
            for label in self.agent_state.memory.list_block_labels():
                updated_value = new_memory.get_block(label).value
                if updated_value != self.agent_state.memory.get_block(label).value:
                    # update the block if it's changed
                    block_id = self.agent_state.memory.get_block(label).id
                    block = self.block_manager.update_block(
                        block_id=block_id, block_update=BlockUpdate(value=updated_value), actor=self.user
                    )

            # refresh memory from luann.DB (using block ids)
            self.agent_state.memory = Memory(
                blocks=[self.block_manager.get_block_by_id(block.id, actor=self.user) for block in self.agent_state.memory.get_blocks()]
            )

            # NOTE: don't do this since re-buildin the memory is handled at the start of the step
            # rebuild memory - this records the last edited timestamp of the memory
            # TODO: pass in update timestamp from luann.block edit time
            self.agent_state = self.agent_manager.rebuild_system_prompt(agent_id=self.agent_state.id, actor=self.user)

            return True
        return False

    def execute_tool_and_persist_state(self, function_name: str, function_args: dict, target_luann_tool: Tool):
        """
        Execute tool modifications and persist the state of the agent.
        Note: only some agent state modifications will be persisted, such as data in the AgentState ORM and block data
        """
        # TODO: add agent manager here
        orig_memory_str = self.agent_state.memory.compile()

        # TODO: need to have an AgentState object that actually has full access to the block data
        # this is because the sandbox tools need to be able to access block.value to edit this data
        try:
            if target_luann_tool.tool_type == ToolType.LUANN_CORE:
                # base tools are allowed to access the `Agent` object and run on the database
                callable_func = get_function_from_module(LUANN_CORE_TOOL_MODULE_NAME, function_name)
                function_args["self"] = self  # need to attach self to arg since it's dynamically linked
                function_response = callable_func(**function_args)
            elif target_luann_tool.tool_type == ToolType.LUANN_MULTI_AGENT_CORE:
                callable_func = get_function_from_module(LUANN_MULTI_AGENT_TOOL_MODULE_NAME, function_name)
                function_args["self"] = self  # need to attach self to arg since it's dynamically linked
                function_response = callable_func(**function_args)
            elif target_luann_tool.tool_type == ToolType.LUANN_MEMORY_CORE:
                callable_func = get_function_from_module(LUANN_CORE_TOOL_MODULE_NAME, function_name)
                agent_state_copy = self.agent_state.__deepcopy__()
                function_args["agent_state"] = agent_state_copy  # need to attach self to arg since it's dynamically linked
                function_response = callable_func(**function_args)
                self.update_memory_if_changed(agent_state_copy.memory)
            else:
                # TODO: Get rid of this. This whole piece is pretty shady, that we exec the function to just get the type hints for args.
                env = {}
                env.update(globals())
                exec(target_luann_tool.source_code, env)
                callable_func = env[target_luann_tool.json_schema["name"]]
                spec = inspect.getfullargspec(callable_func).annotations
                for name, arg in function_args.items():
                    if isinstance(function_args[name], dict):
                        function_args[name] = spec[name](**function_args[name])

                # execute tool in a sandbox
                # TODO: allow agent_state to specify which sandbox to execute tools in
                # TODO: This is only temporary, can remove after we publish a pip package with this object
                agent_state_copy = self.agent_state.__deepcopy__()
                agent_state_copy.tools = []

                sandbox_run_result = ToolExecutionSandbox(function_name, function_args, str(self.user.id)).run(agent_state=agent_state_copy)
                function_response, updated_agent_state = sandbox_run_result.func_return, sandbox_run_result.agent_state
                assert orig_memory_str == self.agent_state.memory.compile(), "Memory should not be modified in a sandbox tool"
                if updated_agent_state is not None:
                    self.update_memory_if_changed(updated_agent_state.memory)
        except Exception as e:
            # Need to catch error here, or else trunction wont happen
            # TODO: modify to function execution error
            function_response = get_friendly_error_msg(
                function_name=function_name, exception_name=type(e).__name__, exception_message=str(e)
            )

        return function_response

    def _get_ai_reply(
        self,
        message_sequence: List[Message],
        function_call: Optional[str] = None,
        first_message: bool = False,
        stream: bool = False,  # TODO move to config?
        empty_response_retry_limit: int = 3,
        backoff_factor: float = 0.5,  # delay multiplier for exponential backoff
        max_delay: float = 10.0,  # max delay between retries
        step_count: Optional[int] = None,
    ) -> ChatCompletionResponse:
        """Get response from luann.LLM API with robust retry mechanism."""

        # allowed_tool_names = self.tool_rules_solver.get_allowed_tool_names(last_function_response=self.last_function_response)
        agent_state_tool_jsons = [t.json_schema for t in self.agent_state.tools]

        allowed_functions = (
            agent_state_tool_jsons
            # if not allowed_tool_names
            # else [func for func in agent_state_tool_jsons if func["name"] in allowed_tool_names]
        )

        # # For the first message, force the initial tool if one is specified
        # force_tool_call = None
        # if (
        #     step_count is not None
        #     and step_count == 0
        #     and not self.supports_structured_output
        #     and len(self.tool_rules_solver.init_tool_rules) > 0
        # ):
        #     force_tool_call = self.tool_rules_solver.init_tool_rules[0].tool_name
        # # Force a tool call if exactly one tool is specified
        # elif step_count is not None and step_count > 0 and len(allowed_tool_names) == 1:
        #     force_tool_call = allowed_tool_names[0]
        for attempt in range(1, empty_response_retry_limit + 1):
            try:
                response = create(
                    llm_config=self.agent_state.llm_config,
                    messages=message_sequence,
                    user_id=self.agent_state.created_by_id,
                    functions=allowed_functions,
                    # functions_python=self.functions_python, do we need this?
                    function_call=function_call,
                    first_message=first_message,
                    # force_tool_call=force_tool_call,
                    stream=stream,
                    stream_interface=self.interface,
                )

                # These bottom two are retryable
                if len(response.choices) == 0 or response.choices[0] is None:
                    raise ValueError(f"API call returned an empty message: {response}")

                if response.choices[0].finish_reason not in ["stop", "function_call", "tool_calls"]:
                    if response.choices[0].finish_reason == "length":
                        # This is not retryable, hence RuntimeError v.s. ValueError
                        raise RuntimeError("Finish reason was length (maximum context length)")
                    else:
                        raise ValueError(f"Bad finish reason from luann.API: {response.choices[0].finish_reason}")

                return response

            except ValueError as ve:
                if attempt >= empty_response_retry_limit:
                    warnings.warn(f"Retry limit reached. Final error: {ve}")
                    raise Exception(f"Retries exhausted and no valid response received. Final error: {ve}")
                else:
                    delay = min(backoff_factor * (2 ** (attempt - 1)), max_delay)
                    warnings.warn(f"Attempt {attempt} failed: {ve}. Retrying in {delay} seconds...")
                    time.sleep(delay)

            except Exception as e:
                # For non-retryable errors, exit immediately
                raise e

        raise Exception("Retries exhausted and no valid response received.")

    def _handle_ai_response(
        self,
        response_message: ChatCompletionMessage,  # TODO should we eventually move the Message creation outside of this function?
        override_tool_call_id: bool = False,
        # If we are streaming, we needed to create a Message ID ahead of time,
        # and now we want to use it in the creation of the Message object
        # TODO figure out a cleaner way to do this
        response_message_id: Optional[str] = None,
    ) -> Tuple[List[Message], bool, bool]:
        """Handles parsing and function execution"""

        # Hacky failsafe for now to make sure we didn't implement the streaming Message ID creation incorrectly
        if response_message_id is not None:
            assert response_message_id.startswith("message-"), response_message_id

        messages = []  # append these to the history when done
        function_name = None

        # Step 2: check if LLM wanted to call a function
        if response_message.function_call or (response_message.tool_calls is not None and len(response_message.tool_calls) > 0):
            if response_message.function_call:
                raise DeprecationWarning(response_message)
            if response_message.tool_calls is not None and len(response_message.tool_calls) > 1:
                # raise NotImplementedError(f">1 tool call not supported")
                # TODO eventually support sequential tool calling
                printd(f">1 tool call not supported, using index=0 only\n{response_message.tool_calls}")
                response_message.tool_calls = [response_message.tool_calls[0]]
            assert response_message.tool_calls is not None and len(response_message.tool_calls) > 0

            # generate UUID for tool call
            if override_tool_call_id or response_message.function_call:
                warnings.warn("Overriding the tool call can result in inconsistent tool call IDs during streaming")
                tool_call_id = get_tool_call_id()  # needs to be a string for JSON
                response_message.tool_calls[0].id = tool_call_id
            else:
                tool_call_id = response_message.tool_calls[0].id
                assert tool_call_id is not None  # should be defined

            # only necessary to add the tool_cal_id to a function call (antipattern)
            # response_message_dict = response_message.model_dump()
            # response_message_dict["tool_call_id"] = tool_call_id

            # role: assistant (requesting tool call, set tool call ID)
            messages.append(
                # NOTE: we're recreating the message here
                # TODO should probably just overwrite the fields?
                Message.dict_to_message(
                    id=response_message_id,
                    agent_id=self.agent_state.id,
                    user_id=self.agent_state.created_by_id,
                    model=self.model,
                    openai_message_dict=response_message.model_dump(),
                )
            )  # extend conversation with assistant's reply
            printd(f"Function call message: {messages[-1]}")

            nonnull_content = False
            if response_message.content:
                # The content if then internal monologue, not chat
                self.interface.internal_monologue(response_message.content, msg_obj=messages[-1])
                # Flag to avoid printing a duplicate if inner thoughts get popped from luann.the function call
                nonnull_content = True

            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            function_call = (
                response_message.function_call if response_message.function_call is not None else response_message.tool_calls[0].function
            )

            # Get the name of the function
            function_name = function_call.name
            printd(f"Request to call function {function_name} with tool_call_id: {tool_call_id}")

            # Failure case 1: function name is wrong (not in agent_state.tools)
            target_luann_tool = None
            for t in self.agent_state.tools:
                if t.name == function_name:
                    target_luann_tool = t

            if not target_luann_tool:
                error_msg = f"No function named {function_name}"
                function_response = package_function_response(False, error_msg)
                messages.append(
                    Message.dict_to_message(
                        agent_id=self.agent_state.id,
                        user_id=self.agent_state.created_by_id,
                        model=self.model,
                        openai_message_dict={
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                            "tool_call_id": tool_call_id,
                        },
                    )
                )  # extend conversation with function response
                self.interface.function_message(f"Error: {error_msg}", msg_obj=messages[-1])
                return messages, False, True  # force a heartbeat to allow agent to handle error

            # Failure case 2: function name is OK, but function args are bad JSON
            try:
                raw_function_args = function_call.arguments
                function_args = parse_json(raw_function_args)
            except Exception:
                error_msg = f"Error parsing JSON for function '{function_name}' arguments: {function_call.arguments}"
                function_response = package_function_response(False, error_msg)
                messages.append(
                    Message.dict_to_message(
                        agent_id=self.agent_state.id,
                        user_id=self.agent_state.created_by_id,
                        model=self.model,
                        openai_message_dict={
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                            "tool_call_id": tool_call_id,
                        },
                    )
                )  # extend conversation with function response
                self.interface.function_message(f"Error: {error_msg}", msg_obj=messages[-1])
                return messages, False, True  # force a heartbeat to allow agent to handle error

            # Check if inner thoughts is in the function call arguments (possible apparently if you are using Azure)
            if "inner_thoughts" in function_args:
                response_message.content = function_args.pop("inner_thoughts")
            # The content if then internal monologue, not chat
            if response_message.content and not nonnull_content:
                self.interface.internal_monologue(response_message.content, msg_obj=messages[-1])

            # (Still parsing function args)
            # Handle requests for immediate heartbeat
            heartbeat_request = function_args.pop("request_heartbeat", None)

            # Edge case: heartbeat_request is returned as a stringified boolean, we will attempt to parse:
            if isinstance(heartbeat_request, str) and heartbeat_request.lower().strip() == "true":
                heartbeat_request = True

            if not isinstance(heartbeat_request, bool) or heartbeat_request is None:
                printd(
                    f"{CLI_WARNING_PREFIX}'request_heartbeat' arg parsed was not a bool or None, type={type(heartbeat_request)}, value={heartbeat_request}"
                )
                heartbeat_request = False

            # Failure case 3: function failed during execution
            # NOTE: the msg_obj associated with the "Running " message is the prior assistant message, not the function/tool role message
            #       this is because the function/tool role message is only created once the function/tool has executed/returned
            self.interface.function_message(f"Running {function_name}({function_args})", msg_obj=messages[-1])
            try:
                # handle tool execution (sandbox) and state updates
                function_response = self.execute_tool_and_persist_state(function_name, function_args, target_luann_tool)

                # handle trunction
                if function_name in ["conversation_search", "conversation_search_date", "archival_memory_search"]:
                    # with certain functions we rely on the paging mechanism to handle overflow
                    truncate = False
                else:
                    # but by default, we add a truncation safeguard to prevent bad functions from
                    # overflow the agent context window
                    truncate = True

                # get the function response limit
                return_char_limit = target_luann_tool.return_char_limit
                function_response_string = validate_function_response(
                    function_response, return_char_limit=return_char_limit, truncate=truncate
                )
                function_args.pop("self", None)
                function_response = package_function_response(True, function_response_string)
                function_failed = False
            except Exception as e:
                function_args.pop("self", None)
                # error_msg = f"Error calling function {function_name} with args {function_args}: {str(e)}"
                # Less detailed - don't provide full args, idea is that it should be in recent context so no need (just adds noise)
                error_msg = get_friendly_error_msg(function_name=function_name, exception_name=type(e).__name__, exception_message=str(e))
                error_msg_user = f"{error_msg}\n{traceback.format_exc()}"
                printd(error_msg_user)
                function_response = package_function_response(False, error_msg)
                self.last_function_response = function_response
                # TODO: truncate error message somehow
                messages.append(
                    Message.dict_to_message(
                        agent_id=self.agent_state.id,
                        user_id=self.agent_state.created_by_id,
                        model=self.model,
                        openai_message_dict={
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                            "tool_call_id": tool_call_id,
                        },
                    )
                )  # extend conversation with function response
                self.interface.function_message(f"Ran {function_name}({function_args})", msg_obj=messages[-1])
                self.interface.function_message(f"Error: {error_msg}", msg_obj=messages[-1])
                return messages, False, True  # force a heartbeat to allow agent to handle error

            # Step 4: check if function response is an error
            if function_response_string.startswith(ERROR_MESSAGE_PREFIX):
                function_response = package_function_response(False, function_response_string)
                # TODO: truncate error message somehow
                messages.append(
                    Message.dict_to_message(
                        agent_id=self.agent_state.id,
                        user_id=self.agent_state.created_by_id,
                        model=self.model,
                        openai_message_dict={
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                            "tool_call_id": tool_call_id,
                        },
                    )
                )  # extend conversation with function response
                self.interface.function_message(f"Ran {function_name}({function_args})", msg_obj=messages[-1])
                self.interface.function_message(f"Error: {function_response_string}", msg_obj=messages[-1])
                return messages, False, True  # force a heartbeat to allow agent to handle error

            # If no failures happened along the way: ...
            # Step 5: send the info on the function call and function response to GPT
            messages.append(
                Message.dict_to_message(
                    agent_id=self.agent_state.id,
                    user_id=self.agent_state.created_by_id,
                    model=self.model,
                    openai_message_dict={
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                        "tool_call_id": tool_call_id,
                    },
                )
            )  # extend conversation with function response
            self.interface.function_message(f"Ran {function_name}({function_args})", msg_obj=messages[-1])
            self.interface.function_message(f"Success: {function_response_string}", msg_obj=messages[-1])
            self.last_function_response = function_response

        else:
            # Standard non-function reply
            messages.append(
                Message.dict_to_message(
                    id=response_message_id,
                    agent_id=self.agent_state.id,
                    user_id=self.agent_state.created_by_id,
                    model=self.model,
                    openai_message_dict=response_message.model_dump(),
                )
            )  # extend conversation with assistant's reply
            self.interface.internal_monologue(response_message.content, msg_obj=messages[-1])
            heartbeat_request = False
            function_failed = False

        # rebuild memory
        # TODO: @charles please check this
        self.agent_state = self.agent_manager.rebuild_system_prompt(agent_id=self.agent_state.id, actor=self.user)

        # Update ToolRulesSolver state with last called function
        # self.tool_rules_solver.update_tool_usage(function_name)
        # Update heartbeat request according to provided tool rules
        # if self.tool_rules_solver.has_children_tools(function_name):
        #     heartbeat_request = True
        # elif self.tool_rules_solver.is_terminal_tool(function_name):
        #     heartbeat_request = False

        return messages, heartbeat_request, function_failed

    def step(
        self,
        messages: Union[Message, List[Message]],
        # additional args
        chaining: bool = True,
        max_chaining_steps: Optional[int] = None,
        **kwargs,
    ) -> LuannUsageStatistics:
        """Run Agent.step in a loop, handling chaining via heartbeat requests and function failures"""
        next_input_message = messages if isinstance(messages, list) else [messages]
        counter = 0
        total_usage = UsageStatistics()
        step_count = 0
        while True:
            kwargs["first_message"] = False
            kwargs["step_count"] = step_count
            step_response = self.inner_step(
                messages=next_input_message,
                **kwargs,
            )

            heartbeat_request = step_response.heartbeat_request
            function_failed = step_response.function_failed
            token_warning = step_response.in_context_memory_warning
            usage = step_response.usage

            step_count += 1
            total_usage += usage
            counter += 1
            self.interface.step_complete()

            # logger.debug("Saving agent state")
            # save updated state
            save_agent(self)

            # Chain stops
            if not chaining:
                printd("No chaining, stopping after one step")
                break
            elif max_chaining_steps is not None and counter > max_chaining_steps:
                printd(f"Hit max chaining steps, stopping after {counter} steps")
                break
            # Chain handlers
            elif token_warning:
                assert self.agent_state.created_by_id is not None
                next_input_message = Message.dict_to_message(
                    agent_id=self.agent_state.id,
                    user_id=self.agent_state.created_by_id,
                    model=self.model,
                    openai_message_dict={
                        "role": "user",  # TODO: change to system?
                        "content": get_token_limit_warning(),
                    },
                )
                continue  # always chain
            elif function_failed:
                assert self.agent_state.created_by_id is not None
                next_input_message = Message.dict_to_message(
                    agent_id=self.agent_state.id,
                    user_id=self.agent_state.created_by_id,
                    model=self.model,
                    openai_message_dict={
                        "role": "user",  # TODO: change to system?
                        "content": get_heartbeat(FUNC_FAILED_HEARTBEAT_MESSAGE),
                    },
                )
                continue  # always chain
            elif heartbeat_request:
                assert self.agent_state.created_by_id is not None
                next_input_message = Message.dict_to_message(
                    agent_id=self.agent_state.id,
                    user_id=self.agent_state.created_by_id,
                    model=self.model,
                    openai_message_dict={
                        "role": "user",  # TODO: change to system?
                        "content": get_heartbeat(REQ_HEARTBEAT_MESSAGE),
                    },
                )
                continue  # always chain
           
            else:
                break

        return LuannUsageStatistics(**total_usage.model_dump(), step_count=step_count)

    def inner_step(
        self,
        messages: Union[Message, List[Message]],
        first_message: bool = False,
        first_message_retry_limit: int = FIRST_MESSAGE_ATTEMPTS,
        skip_verify: bool = False,
        stream: bool = False,  # TODO move to config?
        step_count: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> AgentStepResponse:
        """Runs a single step in the agent loop (generates at most one LLM call)"""

        try:

            # Extract job_id from luann.metadata if present
            # job_id = metadata.get("job_id") if metadata else None

            # Step 0: update core memory
            # only pulling latest block data if shared memory is being used
            current_persisted_memory = Memory(
                blocks=[self.block_manager.get_block_by_id(block.id, actor=self.user) for block in self.agent_state.memory.get_blocks()]
            )  # read blocks from luann.DB
            self.update_memory_if_changed(current_persisted_memory)

            # Step 1: add user message
            if isinstance(messages, Message):
                messages = [messages]

            if not all(isinstance(m, Message) for m in messages):
                raise ValueError(f"messages should be a Message or a list of Message, got {type(messages)}")

            in_context_messages = self.agent_manager.get_in_context_messages(agent_id=self.agent_state.id, actor=self.user)
            input_message_sequence = in_context_messages + messages

            if len(input_message_sequence) > 1 and input_message_sequence[-1].role != "user":
                printd(f"{CLI_WARNING_PREFIX}Attempting to run ChatCompletion without user as the last message in the queue")

            # Step 2: send the conversation and available functions to the LLM
            response = self._get_ai_reply(
                message_sequence=input_message_sequence,
                first_message=first_message,
                stream=stream,
                step_count=step_count,
            )
            # print(f"llm response:{response}")
            # Step 3: check if LLM wanted to call a function
            # (if yes) Step 4: call the function
            # (if yes) Step 5: send the info on the function call and function response to LLM
            response_message = response.choices[0].message
            response_message.model_copy()  # TODO why are we copying here?
            all_response_messages, heartbeat_request, function_failed = self._handle_ai_response(
                response_message,
                # TODO this is kind of hacky, find a better way to handle this
                # the only time we set up message creation ahead of time is when streaming is on
                response_message_id=response.id if stream else None,
            )

            # Step 6: extend the message history
            if len(messages) > 0:
                all_new_messages = messages + all_response_messages
            else:
                all_new_messages = all_response_messages

            # Check the memory pressure and potentially issue a memory pressure warning
            current_total_tokens = response.usage.total_tokens
            active_memory_warning = False

            # We can't do summarize logic properly if context_window is undefined
            if self.agent_state.llm_config.context_window is None:
                # Fallback if for some reason context_window is missing, just set to the default
                print(f"{CLI_WARNING_PREFIX}could not find context_window in config, setting to default {LLM_MAX_TOKENS['DEFAULT']}")
                print(f"{self.agent_state}")
                self.agent_state.llm_config.context_window = (
                    LLM_MAX_TOKENS[self.model] if (self.model is not None and self.model in LLM_MAX_TOKENS) else LLM_MAX_TOKENS["DEFAULT"]
                )

            if current_total_tokens > MESSAGE_SUMMARY_WARNING_FRAC * int(self.agent_state.llm_config.context_window):
                printd(
                    f"{CLI_WARNING_PREFIX}last response total_tokens ({current_total_tokens}) > {MESSAGE_SUMMARY_WARNING_FRAC * int(self.agent_state.llm_config.context_window)}"
                )

                # Only deliver the alert if we haven't already (this period)
                if not self.agent_alerted_about_memory_pressure:
                    active_memory_warning = True
                    self.agent_alerted_about_memory_pressure = True  # it's up to the outer loop to handle this

            else:
                printd(
                    f"last response total_tokens ({current_total_tokens}) < {MESSAGE_SUMMARY_WARNING_FRAC * int(self.agent_state.llm_config.context_window)}"
                )

            # Persisting into Messages
            self.agent_state = self.agent_manager.append_to_in_context_messages(
                all_new_messages, agent_id=self.agent_state.id, actor=self.user
            )
            # if job_id:
            #     for message in all_new_messages:
            #         self.job_manager.add_message_to_job(
            #             job_id=job_id,
            #             message_id=message.id,
            #             actor=self.user,
            #         )

            return AgentStepResponse(
                messages=all_new_messages,
                heartbeat_request=heartbeat_request,
                function_failed=function_failed,
                in_context_memory_warning=active_memory_warning,
                usage=response.usage,
            )

        except Exception as e:
            printd(f"step() failed\nmessages = {messages}\nerror = {e}")

            # If we got a context alert, try trimming the messages length, then try again
            if is_context_overflow_error(e):
                printd(
                    f"context window exceeded with limit {self.agent_state.llm_config.context_window}, running summarizer to trim messages"
                )
                # A separate API call to run a summarizer
                self.summarize_messages_inplace()

                # Try step again
                return self.inner_step(
                    messages=messages,
                    first_message=first_message,
                    first_message_retry_limit=first_message_retry_limit,
                    skip_verify=skip_verify,
                    stream=stream,
                    metadata=metadata,
                )

            else:
                printd(f"step() failed with an unrecognized exception: '{str(e)}'")
                raise e

    def step_user_message(self, user_message_str: str, **kwargs) -> AgentStepResponse:
        """Takes a basic user message string, turns it into a stringified JSON with extra metadata, then sends it to the agent

        Example:
        -> user_message_str = 'hi'
        -> {'message': 'hi', 'type': 'user_message', ...}
        -> json.dumps(...)
        -> agent.step(messages=[Message(role='user', text=...)])
        """
        # Wrap with metadata, dumps to JSON
        assert user_message_str and isinstance(
            user_message_str, str
        ), f"user_message_str should be a non-empty string, got {type(user_message_str)}"
        user_message_json_str = package_user_message(user_message_str)

        # Validate JSON via save/load
        user_message = validate_json(user_message_json_str)
        cleaned_user_message_text, name = strip_name_field_from_user_message(user_message)

        # Turn into a dict
        openai_message_dict = {"role": "user", "content": cleaned_user_message_text, "name": name}

        # Create the associated Message object (in the database)
        assert self.agent_state.created_by_id is not None, "User ID is not set"
        user_message = Message.dict_to_message(
            agent_id=self.agent_state.id,
            user_id=self.agent_state.created_by_id,
            model=self.model,
            openai_message_dict=openai_message_dict,
            # created_at=timestamp,
        )

        return self.inner_step(messages=[user_message], **kwargs)

    def summarize_messages_inplace(self):
        in_context_messages = self.agent_manager.get_in_context_messages(agent_id=self.agent_state.id, actor=self.user)
        in_context_messages_openai = [m.to_openai_dict() for m in in_context_messages]
        in_context_messages_openai_no_system = in_context_messages_openai[1:]
        token_counts = get_token_counts_for_messages(in_context_messages)
        logger.info(f"System message token count={token_counts[0]}")
        logger.info(f"token_counts_no_system={token_counts[1:]}")

        if in_context_messages_openai[0]["role"] != "system":
            raise RuntimeError(f"in_context_messages_openai[0] should be system (instead got {in_context_messages_openai[0]})")

        # If at this point there's nothing to summarize, throw an error
        if len(in_context_messages_openai_no_system) == 0:
            raise ContextWindowExceededError(
                "Not enough messages to compress for summarization",
                details={
                    "num_candidate_messages": len(in_context_messages_openai_no_system),
                    "num_total_messages": len(in_context_messages_openai),
                },
            )

        cutoff = calculate_summarizer_cutoff(in_context_messages=in_context_messages, token_counts=token_counts, logger=logger)
        message_sequence_to_summarize = in_context_messages[1:cutoff]  # do NOT get rid of the system message
        logger.info(f"Attempting to summarize {len(message_sequence_to_summarize)} messages of {len(in_context_messages)}")

        # We can't do summarize logic properly if context_window is undefined
        if self.agent_state.llm_config.context_window is None:
            # Fallback if for some reason context_window is missing, just set to the default
            logger.warning(f"{CLI_WARNING_PREFIX}could not find context_window in config, setting to default {LLM_MAX_TOKENS['DEFAULT']}")
            self.agent_state.llm_config.context_window = (
                LLM_MAX_TOKENS[self.model] if (self.model is not None and self.model in LLM_MAX_TOKENS) else LLM_MAX_TOKENS["DEFAULT"]
            )

        summary = summarize_messages(agent_state=self.agent_state, message_sequence_to_summarize=message_sequence_to_summarize)
        logger.info(f"Got summary: {summary}")

        # Metadata that's useful for the agent to see
        all_time_message_count = self.message_manager.size(agent_id=self.agent_state.id, actor=self.user)
        remaining_message_count = 1 + len(in_context_messages) - cutoff  # System + remaining
        hidden_message_count = all_time_message_count - remaining_message_count
        summary_message_count = len(message_sequence_to_summarize)
        summary_message = package_summarize_message(summary, summary_message_count, hidden_message_count, all_time_message_count)
        logger.info(f"Packaged into message: {summary_message}")

        prior_len = len(in_context_messages_openai)
        self.agent_state = self.agent_manager.trim_all_in_context_messages_except_system(agent_id=self.agent_state.id, actor=self.user)
        packed_summary_message = {"role": "user", "content": summary_message}
        # Prepend the summary
        self.agent_state = self.agent_manager.prepend_to_in_context_messages(
            messages=[
                Message.dict_to_message(
                    agent_id=self.agent_state.id,
                    user_id=self.agent_state.created_by_id,
                    model=self.model,
                    openai_message_dict=packed_summary_message,
                )
            ],
            agent_id=self.agent_state.id,
            actor=self.user,
        )

        # reset alert
        self.agent_alerted_about_memory_pressure = False
        curr_in_context_messages = self.agent_manager.get_in_context_messages(agent_id=self.agent_state.id, actor=self.user)

        logger.info(f"Ran summarizer, messages length {prior_len} -> {len(curr_in_context_messages)}")
        logger.info(
            f"Summarizer brought down total token count from luann.{sum(token_counts)} -> {sum(get_token_counts_for_messages(curr_in_context_messages))}"
        )

    def add_function(self, function_name: str) -> str:
        # TODO: refactor
        raise NotImplementedError

    def remove_function(self, function_name: str) -> str:
        # TODO: refactor
        raise NotImplementedError

    def migrate_embedding(self, embedding_config: EmbeddingConfig):
        """Migrate the agent to a new embedding"""
        # TODO: archival memory

        # TODO: recall memory
        raise NotImplementedError()

    def get_context_window(self) -> ContextWindowOverview:
        """Get the context window of the agent"""

        system_prompt = self.agent_state.system  # TODO is this the current system or the initial system?
        # print(f"system_prompt:{system_prompt}")
        num_tokens_system = count_tokens(system_prompt)
        # print(f"num_tokens_system:{num_tokens_system}")
        core_memory = self.agent_state.memory.compile()
        # print(f"core_memory:{core_memory}")
        
        num_tokens_core_memory = count_tokens(core_memory)
        # print(f"num_tokens_core_memory:{num_tokens_core_memory}")
        # Grab the in-context messages
        # conversion of messages to OpenAI dict format, which is passed to the token counter
        in_context_messages = self.agent_manager.get_in_context_messages(agent_id=self.agent_state.id, actor=self.user)
        # print(f"in_context_messages:{in_context_messages}")
        in_context_messages_openai = [m.to_openai_dict() for m in in_context_messages]
        # print(f"in_context_messages_openai:{in_context_messages_openai}")
        # Check if there's a summary message in the message queue
        if (
            len(in_context_messages) > 1
            and in_context_messages[1].role == MessageRole.user
            and isinstance(in_context_messages[1].text, str)
            # TODO remove hardcoding
            and "The following is a summary of the previous " in in_context_messages[1].text
        ):
            # Summary message exists
            assert in_context_messages[1].text is not None
            summary_memory = in_context_messages[1].text
            num_tokens_summary_memory = count_tokens(in_context_messages[1].text)
            # with a summary message, the real messages start at index 2
            num_tokens_messages = (
                num_tokens_from_messages(messages=in_context_messages_openai[2:], model=self.model)
                if len(in_context_messages_openai) > 2
                else 0
            )

        else:
            summary_memory = None
            num_tokens_summary_memory = 0
            # with no summary message, the real messages start at index 1
            num_tokens_messages = (
                num_tokens_from_messages(messages=in_context_messages_openai[1:], model=self.model)
                if len(in_context_messages_openai) > 1
                else 0
            )
        
        # print(f"summary_memory:{summary_memory}")
        # print(f"num_tokens_summary_memory:{num_tokens_summary_memory}")

        # print(f"num_tokens_from_messages:{num_tokens_messages}")
        agent_manager_passage_size = self.agent_manager.passage_size(actor=self.user, agent_id=self.agent_state.id)
        # print(f"agent_manager_passage_size:{agent_manager_passage_size}")
        message_manager_size = self.message_manager.size(actor=self.user, agent_id=self.agent_state.id)

        # print(f"message_manager_size:{message_manager_size}")/
        external_memory_summary = compile_memory_metadata_block(
            memory_edit_timestamp=get_utc_time(),
            previous_message_count=self.message_manager.size(actor=self.user, agent_id=self.agent_state.id),
            archival_memory_size=self.agent_manager.passage_size(actor=self.user, agent_id=self.agent_state.id),
        )

        # print(f"external_memory_summary:{external_memory_summary}")
        num_tokens_external_memory_summary = count_tokens(external_memory_summary)

        # print(f"num_tokens_external_memory_summary:{num_tokens_external_memory_summary}")

        # tokens taken up by function definitions
        agent_state_tool_jsons = [t.json_schema for t in self.agent_state.tools]

        # print(f"agent_state_tool_jsons:{agent_state_tool_jsons}")
        if agent_state_tool_jsons:
            available_functions_definitions = [OpenAITool(type="function", function=f) for f in agent_state_tool_jsons]
            num_tokens_available_functions_definitions = num_tokens_from_functions(functions=agent_state_tool_jsons, model=self.model)
        else:
            available_functions_definitions = []
            num_tokens_available_functions_definitions = 0
        

        # print(f"available_functions_definitions:{available_functions_definitions}")
        # print(f"num_tokens_available_functions_definitions:{num_tokens_available_functions_definitions}")
        num_tokens_used_total = (
            num_tokens_system  # system prompt
            + num_tokens_available_functions_definitions  # function definitions
            + num_tokens_core_memory  # core memory
            + num_tokens_external_memory_summary  # metadata (statistics) about recall/archival
            + num_tokens_summary_memory  # summary of ongoing conversation
            + num_tokens_messages  # tokens taken by messages
        )
        assert isinstance(num_tokens_used_total, int)
        # print(f"num_tokens_used_total:{num_tokens_used_total}")
        return ContextWindowOverview(
            # context window breakdown (in messages)
            num_messages=len(in_context_messages),
            num_archival_memory=agent_manager_passage_size,
            num_recall_memory=message_manager_size,
            num_tokens_external_memory_summary=num_tokens_external_memory_summary,
            external_memory_summary=external_memory_summary,
            # top-level information
            context_window_size_max=self.agent_state.llm_config.context_window,
            context_window_size_current=num_tokens_used_total,
            # context window breakdown (in tokens)
            num_tokens_system=num_tokens_system,
            system_prompt=system_prompt,
            num_tokens_core_memory=num_tokens_core_memory,
            core_memory=core_memory,
            num_tokens_summary_memory=num_tokens_summary_memory,
            summary_memory=summary_memory,
            num_tokens_messages=num_tokens_messages,
            messages=in_context_messages,
            # related to functions
            num_tokens_functions_definitions=num_tokens_available_functions_definitions,
            functions_definitions=available_functions_definitions,
        )

    def count_tokens(self) -> int:
        """Count the tokens in the current context window"""
        context_window_breakdown = self.get_context_window()
        return context_window_breakdown.context_window_size_current


def save_agent(agent: Agent):
    """Save agent to metadata store"""
    agent_state = agent.agent_state
    assert isinstance(agent_state.memory, Memory), f"Memory is not a Memory object: {type(agent_state.memory)}"

    # TODO: move this to agent manager
    # TODO: Completely strip out metadata
    # convert to persisted model
    agent_manager = AgentManager()
    update_agent = UpdateAgent(
        name=agent_state.name,
        tool_ids=[t.id for t in agent_state.tools],
        source_ids=[s.id for s in agent_state.sources],
        block_ids=[b.id for b in agent_state.memory.blocks],
        tags=agent_state.tags,
        system=agent_state.system,
        # tool_rules=agent_state.tool_rules,
        llm_config=agent_state.llm_config,
        embedding_config=agent_state.embedding_config,
        message_ids=agent_state.message_ids,
        description=agent_state.description,
        metadata_=agent_state.metadata_,
        # TODO: Add this back in later
        # tool_exec_environment_variables=agent_state.get_agent_env_vars_as_dict(),
    )
    agent_manager.update_agent(agent_id=agent_state.id, agent_update=update_agent, actor=agent.user)


def strip_name_field_from_user_message(user_message_text: str) -> Tuple[str, Optional[str]]:
    """If 'name' exists in the JSON string, remove it and return the cleaned text + name value"""
    try:
        user_message_json = dict(json_loads(user_message_text))
        # Special handling for AutoGen messages with 'name' field
        # Treat 'name' as a special field
        # If it exists in the input message, elevate it to the 'message' level
        name = user_message_json.pop("name", None)
        clean_message = json_dumps(user_message_json)
        return clean_message, name

    except Exception as e:
        print(f"{CLI_WARNING_PREFIX}handling of 'name' field failed with: {e}")
        raise e


def validate_json(user_message_text: str) -> str:
    """Make sure that the user input message is valid JSON"""
    try:
        user_message_json = dict(json_loads(user_message_text))
        user_message_json_val = json_dumps(user_message_json)
        return user_message_json_val
    except Exception as e:
        print(f"{CLI_WARNING_PREFIX}couldn't parse user input message as JSON: {e}")
        raise e
