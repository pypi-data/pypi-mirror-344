import random
import time
from typing import List, Optional, Union

import requests

from luann.constants import CLI_WARNING_PREFIX
from luann.errors import LuannConfigurationError, RateLimitExceededError
from luann.llm_api.anthropic import (

    anthropic_chat_completions_request,
)
from luann.llm_api.azure_openai import azure_openai_chat_completions_request
from luann.llm_api.google_ai import convert_tools_to_google_ai_format, google_ai_chat_completions_request
from luann.llm_api.helpers import  unpack_all_inner_thoughts_from_kwargs
from luann.llm_api.openai import (
    build_openai_chat_completions_request,
    openai_chat_completions_process_stream,
    openai_chat_completions_request,
)
from luann.local_llm.chat_completion_proxy import get_chat_completion
from luann.local_llm.constants import INNER_THOUGHTS_KWARG
from luann.local_llm.utils import num_tokens_from_functions, num_tokens_from_messages
from luann.schemas.llm_config import LLMConfig
from luann.schemas.message import Message
from luann.schemas.openai.chat_completion_request import ChatCompletionRequest, Tool, cast_message_to_subtype
from luann.schemas.openai.chat_completion_response import ChatCompletionResponse
from luann.services.provider_manager import ProviderManager
from luann.settings import ModelSettings
from luann.streaming_interface import AgentChunkStreamingInterface, AgentRefreshStreamingInterface

LLM_API_PROVIDER_OPTIONS = ["openai", "azure", "anthropic", "google_ai", "local",]


def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 20,
    # List of OpenAI error codes: https://github.com/openai/openai-python/blob/17ac6779958b2b74999c634c4ea4c7b74906027a/src/openai/_client.py#L227-L250
    # 429 = rate limit
    error_codes: tuple = (429,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        pass

        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            except requests.exceptions.HTTPError as http_err:

                if not hasattr(http_err, "response") or not http_err.response:
                    raise

                # Retry on specified errors
                if http_err.response.status_code in error_codes:
                    # Increment retries
                    num_retries += 1

                    # Check if max retries has been reached
                    if num_retries > max_retries:
                        raise RateLimitExceededError("Maximum number of retries exceeded", max_retries=max_retries)

                    # Increment the delay
                    delay *= exponential_base * (1 + jitter * random.random())

                    # Sleep for the delay
                    # printd(f"Got a rate limit error ('{http_err}') on LLM backend request, waiting {int(delay)}s then retrying...")
                    print(
                        f"{CLI_WARNING_PREFIX}Got a rate limit error ('{http_err}') on LLM backend request, waiting {int(delay)}s then retrying..."
                    )
                    time.sleep(delay)
                else:
                    # For other HTTP errors, re-raise the exception
                    raise

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper


@retry_with_exponential_backoff
def create(
    # agent_state: AgentState,
    llm_config: LLMConfig,
    messages: List[Message],
    user_id: Optional[str] = None,  # option UUID to associate request with
    functions: Optional[list] = None,
    functions_python: Optional[dict] = None,
    function_call: Optional[str] = None,  # see: https://platform.openai.com/docs/api-reference/chat/create#chat-create-tool_choice
    # hint
    first_message: bool = False,
    # force_tool_call: Optional[str] = None,  # Force a specific tool to be called
    # use tool naming?
    # if false, will use deprecated 'functions' style
    use_tool_naming: bool = True,
    # streaming?
    stream: bool = False,
    stream_interface: Optional[Union[AgentRefreshStreamingInterface, AgentChunkStreamingInterface]] = None,
    max_tokens: Optional[int] = None,
    # model_settings: Optional[dict] = None,  # TODO: eventually pass from luann.server
) -> ChatCompletionResponse:
    """Return response to chat completion with backoff"""
    from luann.utils import printd

    # Count the tokens first, if there's an overflow exit early by throwing an error up the stack
    # NOTE: we want to include a specific substring in the error message to trigger summarization
    messages_oai_format = [m.to_openai_dict() for m in messages]
    prompt_tokens = num_tokens_from_messages(messages=messages_oai_format, model=llm_config.model)
    function_tokens = num_tokens_from_functions(functions=functions, model=llm_config.model) if functions else 0
    if prompt_tokens + function_tokens > llm_config.context_window:
        raise Exception(f"Request exceeds maximum context length ({prompt_tokens + function_tokens} > {llm_config.context_window} tokens)")

    # if not model_settings:
    #     from luann.settings import model_settings

    #     model_settings = model_settings
    #     assert isinstance(model_settings, ModelSettings)

    printd(f"Using model {llm_config.model_endpoint_type}, endpoint: {llm_config.model_endpoint}")

    if function_call and not functions:
        printd("unsetting function_call because functions is None")
        function_call = None

    # openai
    if llm_config.model_endpoint_type == "openai":

        if llm_config.openai_api_key is None and llm_config.model_endpoint == "https://api.openai.com/v1":
            # only is a problem if we are *not* using an openai proxy
            raise LuannConfigurationError(message="OpenAI key is missing from luann.luann config file", missing_fields=["openai_api_key"])

        if function_call is None and functions is not None and len(functions) > 0:
            # force function calling for reliability, see https://platform.openai.com/docs/api-reference/chat/create#chat-create-tool_choice
            # TODO(matt) move into LLMConfig
            if llm_config.model_endpoint == "https://inference.memgpt.ai":
                function_call = "auto"  # TODO change to "required" once proxy supports it
            else:
                function_call = "required"

        data = build_openai_chat_completions_request(llm_config, messages, user_id, functions, function_call, use_tool_naming, max_tokens)
        if stream:  # Client requested token streaming
            data.stream = True
            assert isinstance(stream_interface, AgentChunkStreamingInterface) or isinstance(
                stream_interface, AgentRefreshStreamingInterface
            ), type(stream_interface)
            response = openai_chat_completions_process_stream(
                url=llm_config.model_endpoint,  # https://api.openai.com/v1 -> https://api.openai.com/v1/chat/completions
                api_key=llm_config.openai_api_key,
                chat_completion_request=data,
                stream_interface=stream_interface,
            )
        else:  # Client did not request token streaming (expect a blocking backend response)
            data.stream = False
            if isinstance(stream_interface, AgentChunkStreamingInterface):
                stream_interface.stream_start()
            try:
                response = openai_chat_completions_request(
                    url=llm_config.model_endpoint,  # https://api.openai.com/v1 -> https://api.openai.com/v1/chat/completions
                    api_key=llm_config.openai_api_key,
                    chat_completion_request=data,
                )
            finally:
                if isinstance(stream_interface, AgentChunkStreamingInterface):
                    stream_interface.stream_end()

        if llm_config.put_inner_thoughts_in_kwargs:
            response = unpack_all_inner_thoughts_from_kwargs(response=response, inner_thoughts_key=INNER_THOUGHTS_KWARG)

        return response

    # azure
    elif llm_config.model_endpoint_type == "azure":
        if stream:
            raise NotImplementedError(f"Streaming not yet implemented for {llm_config.model_endpoint_type}")

        # if model_settings.azure_api_key is None:
        #     raise LuannConfigurationError(
        #         message="Azure API key is missing. Did you set AZURE_API_KEY in your env?", missing_fields=["azure_api_key"]
        #     )

        # if model_settings.azure_base_url is None:
        #     raise LuannConfigurationError(
        #         message="Azure base url is missing. Did you set AZURE_BASE_URL in your env?", missing_fields=["azure_base_url"]
        #     )

        # if model_settings.azure_api_version is None:
        #     raise LuannConfigurationError(
        #         message="Azure API version is missing. Did you set AZURE_API_VERSION in your env?", missing_fields=["azure_api_version"]
        #     )

        # Set the llm config model_endpoint from luann.model_settings
        # For Azure, this model_endpoint is required to be configured via env variable, so users don't need to provide it in the LLM config
        # llm_config.model_endpoint = model_settings.azure_base_url
        chat_completion_request = build_openai_chat_completions_request(
            llm_config, messages, user_id, functions, function_call, use_tool_naming, max_tokens
        )

        response = azure_openai_chat_completions_request(
            # model_settings=model_settings,
            llm_config=llm_config,
            api_key=llm_config.azure_api_key,
            chat_completion_request=chat_completion_request,
        )

        if llm_config.put_inner_thoughts_in_kwargs:
            response = unpack_all_inner_thoughts_from_kwargs(response=response, inner_thoughts_key=INNER_THOUGHTS_KWARG)

        return response

    elif llm_config.model_endpoint_type == "google_ai":
        if stream:
            raise NotImplementedError(f"Streaming not yet implemented for {llm_config.model_endpoint_type}")
        if not use_tool_naming:
            raise NotImplementedError("Only tool calling supported on Google AI API requests")

        if functions is not None:
            tools = [{"type": "function", "function": f} for f in functions]
            tools = [Tool(**t) for t in tools]
            tools = convert_tools_to_google_ai_format(tools, inner_thoughts_in_kwargs=llm_config.put_inner_thoughts_in_kwargs)
        else:
            tools = None

        return google_ai_chat_completions_request(
            base_url=llm_config.model_endpoint,
            model=llm_config.model,
            api_key=llm_config.googleai_api_key,
            # see structure of payload here: https://ai.google.dev/docs/function_calling
            data=dict(
                contents=[m.to_google_ai_dict() for m in messages],
                tools=tools,
            ),
            inner_thoughts_in_kwargs=llm_config.put_inner_thoughts_in_kwargs,
        )

    elif llm_config.model_endpoint_type == "anthropic":
        if stream:
            raise NotImplementedError(f"Streaming not yet implemented for {llm_config.model_endpoint_type}")
        if not use_tool_naming:
            raise NotImplementedError("Only tool calling supported on Anthropic API requests")

        tool_call = None
        # if force_tool_call is not None:
        #     tool_call = {"type": "function", "function": {"name": force_tool_call}}
        #     assert functions is not None

        # load anthropic key from luann.db in case a custom key has been stored
        # anthropic_key_override = ProviderManager().get_anthropic_override_key()

        return anthropic_chat_completions_request(
            url=llm_config.model_endpoint,
            api_key=llm_config.anthropic_api_key,
            data=ChatCompletionRequest(
                model=llm_config.model,
                messages=[cast_message_to_subtype(m.to_openai_dict()) for m in messages],
                tools=[{"type": "function", "function": f} for f in functions] if functions else None,
                tool_choice=tool_call,
                # user=str(user_id),
                # NOTE: max_tokens is required for Anthropic API
                max_tokens=1024,  # TODO make dynamic
            ),
        )
    

    # local model
    else:
        if stream:
            raise NotImplementedError(f"Streaming not yet implemented for {llm_config.model_endpoint_type}")
        return get_chat_completion(
            model=llm_config.model,
            messages=messages,
            functions=functions,
            functions_python=functions_python,
            function_call=function_call,
            context_window=llm_config.context_window,
            endpoint=llm_config.model_endpoint,
            endpoint_type=llm_config.model_endpoint_type,
            wrapper=llm_config.model_wrapper,
            user=str(user_id),
            # hint
            first_message=first_message,
            # auth-related
            auth_type=llm_config.model_endpoint_type,
            auth_key=llm_config.openllm_api_key,
        )
