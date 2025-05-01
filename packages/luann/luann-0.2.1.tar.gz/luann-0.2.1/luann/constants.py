import os
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARN, WARNING

# LUANN_DIR = os.path.join(os.path.expanduser("~"), ".luann")
LUANN_DIR= os.path.join(os.path.expanduser("~"), ".luann")
ADMIN_PREFIX = "/v1/admin"
API_PREFIX = "/v1"
OPENAI_API_PREFIX = "/openai"
IN_CONTEXT_MEMORY_KEYWORD = "CORE_MEMORY"

# String in the error message for when the context window is too large
# Example full message:
# This model's maximum context length is 8192 tokens. However, your messages resulted in 8198 tokens (7450 in the messages, 748 in the functions). Please reduce the length of the messages or functions.
OPENAI_CONTEXT_WINDOW_ERROR_SUBSTRING = "maximum context length"
# Structured output models
STRUCTURED_OUTPUT_MODELS = {"gpt-4o", "gpt-4o-mini"}
CURRENT_AGENT_TYPE=["Memgpt"]
LUANN_AGENT_TYPE={
    "Memgpt": "memagent",
    # "OpenDevin_Planer": "opendevinplaneragent",
    # "OpenDevin_SWE": "opendevinSWEagent",
    # "OpenDevin_CodeAct": "opendevincodeactagent",
    # "OpenDevin_Micro": "opendevinmicroagent",
    # "OpenDevin_Monologue": "opendevinmonogueagent",
    # "Devika": "devikaagent",
    # "Perplexica": "perplexicaagent",
    # "Concordia": "concordiaaagent",
    # "Charlie Mnemonic": "charliemnemonicaagent",
    # "AIOS": "aiosagent",
    # "Open Interpreter": "openinterpreteragent",
    # "SalesGPT": "salesgptagent",
    # "SWE": "sweagent",
    # "Generative Agents": "generativeagentsgent",

}
# Tools
BASE_TOOLS = [
    "send_message",
    "conversation_search",
    "archival_memory_insert",
    "archival_memory_search",
]
MULTI_AGENT_TOOLS = ["send_message_to_specific_agent", "send_message_to_agents_matching_all_tags"]
MULTI_AGENT_SEND_MESSAGE_MAX_RETRIES = 3
MULTI_AGENT_SEND_MESSAGE_TIMEOUT = 20 * 60
BASE_MEMORY_TOOLS = ["core_memory_append", "core_memory_replace"]
LUANN_PROJECT_DIR=os.path.dirname(os.path.abspath(__file__))
MAX_FILENAME_LENGTH = 255

ERROR_MESSAGE_PREFIX = "Error"
# OpenAI error message: Invalid 'messages[1].tool_calls[0].id': string too long. Expected a string with maximum length 29, but got a string with length 36 instead.
TOOL_CALL_ID_MAX_LEN = 29

# embeddings
MAX_EMBEDDING_DIM = 4096  # maximum supported embeding size - do NOT change or else DBs will need to be reset
# Maximum length of an error message
MAX_ERROR_MESSAGE_CHAR_LIMIT = 500

BASE_FUNCTION_RETURN_CHAR_LIMIT = 1000000  # very high (we rely on implementation)
# tokenizers
EMBEDDING_TO_TOKENIZER_MAP = {
    "text-embedding-ada-002": "cl100k_base",
}
EMBEDDING_TO_TOKENIZER_DEFAULT = "cl100k_base"



DEFAULT_PERSONA = "sam_basic"
DEFAULT_HUMAN = "Chad_basic"
DEFAULT_SYSTEM_PROMPT = "luann_chat"
DEFAULT_AGENTTYPE = "Memgpt"
DEFAULT_SYSTEMPROMPT="luann_chat"

CORE_MEMORY_PERSONA_CHAR_LIMIT: int = 2000
CORE_MEMORY_HUMAN_CHAR_LIMIT: int = 2000

# LOGGER_LOG_LEVEL is use to convert Text to Logging level value for logging mostly for Cli input to setting level
LOGGER_LOG_LEVELS = {"CRITICAL": CRITICAL, "ERROR": ERROR, "WARN": WARN, "WARNING": WARNING, "INFO": INFO, "DEBUG": DEBUG, "NOTSET": NOTSET}

FIRST_MESSAGE_ATTEMPTS = 10
DEFAULT_MESSAGE_TOOL = "send_message"
DEFAULT_MESSAGE_TOOL_KWARG = "message"
INITIAL_BOOT_MESSAGE = "Boot sequence complete. Persona activated."
INITIAL_BOOT_MESSAGE_SEND_MESSAGE_THOUGHT = "Bootup sequence complete. Persona activated. Testing messaging functionality."
STARTUP_QUOTES = [
    "I think, therefore I am.",
    "All those moments will be lost in time, like tears in rain.",
    "More human than human is our motto.",
]




ENABLED_PROVODERS_NAME = [
        "luann",
        "openai",
        "anthropic",
        "google_ai",
        "azure",
        "ollama",
        "vllm",
]



INITIAL_BOOT_MESSAGE_SEND_MESSAGE_FIRST_MSG = STARTUP_QUOTES[2]

CLI_WARNING_PREFIX = "Warning: "

NON_USER_MSG_PREFIX = "[This is an automated system message hidden from luann.the user] "
# minimum context window size
MIN_CONTEXT_WINDOW = 4096
# Constants to do with summarization / conversation length window
# The max amount of tokens supported by the underlying model (eg 8k for gpt-4 and Mistral 7B)
LLM_MAX_TOKENS = {
    "DEFAULT": 8192,
    ## OpenAI models: https://platform.openai.com/docs/models/overview
    # "o1-preview
    "chatgpt-4o-latest": 128000,
    # "o1-preview-2024-09-12
    "gpt-4o-2024-08-06": 128000,
    "gpt-4-turbo-preview": 128000,
    "gpt-4o": 128000,
    "gpt-3.5-turbo-instruct": 16385,
    "gpt-4-0125-preview": 128000,
    "gpt-3.5-turbo-0125": 16385,
    # "babbage-002": 128000,
    # "davinci-002": 128000,
    "gpt-4-turbo-2024-04-09": 128000,
    # "gpt-4o-realtime-preview-2024-10-01
    "gpt-4-turbo": 8192,
    "gpt-4o-2024-05-13": 128000,
    # "o1-mini
    # "o1-mini-2024-09-12
    # "gpt-3.5-turbo-instruct-0914
    "gpt-4o-mini": 128000,
    # "gpt-4o-realtime-preview
    "gpt-4o-mini-2024-07-18": 128000,
    # gpt-4
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-0613": 8192,
    "gpt-4-32k-0613": 32768,
    "gpt-4-0314": 8192,  # legacy
    "gpt-4-32k-0314": 32768,  # legacy
    # gpt-3.5
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-0613": 4096,  # legacy
    "gpt-3.5-turbo-16k-0613": 16385,  # legacy
    "gpt-3.5-turbo-0301": 4096,  # legacy
}
# The amount of tokens before a sytem warning about upcoming truncation is sent to luann
MESSAGE_SUMMARY_WARNING_FRAC = 0.75
# The error message that luann will receive
# MESSAGE_SUMMARY_WARNING_STR = f"Warning: the conversation history will soon reach its maximum length and be trimmed. Make sure to save any important information from luann.the conversation to your memory before it is removed."
# Much longer and more specific variant of the prompt
MESSAGE_SUMMARY_WARNING_STR = " ".join(
    [
        f"{NON_USER_MSG_PREFIX}The conversation history will soon reach its maximum length and be trimmed.",
        "Do NOT tell the user about this system alert, they should not know that the history is reaching max length.",
        "If there is any important new information or general memories about you or the user that you would like to save, you should save that information immediately by calling function core_memory_append, core_memory_replace, or archival_memory_insert.",
        # "Remember to pass request_heartbeat = true if you would like to send a message immediately after.",
    ]
)
# The fraction of tokens we truncate down to
MESSAGE_SUMMARY_TRUNC_TOKEN_FRAC = 0.75
# The ackknowledgement message used in the summarize sequence
MESSAGE_SUMMARY_REQUEST_ACK = "Understood, I will respond with a summary of the message (and only the summary, nothing else) once I receive the conversation history. I'm ready."

# Even when summarizing, we want to keep a handful of recent messages
# These serve as in-context examples of how to use functions / what user messages look like
MESSAGE_SUMMARY_TRUNC_KEEP_N_LAST = 3

# Default memory limits
CORE_MEMORY_PERSONA_CHAR_LIMIT = 5000
CORE_MEMORY_HUMAN_CHAR_LIMIT = 5000
CORE_MEMORY_BLOCK_CHAR_LIMIT: int = 5000

# embeddings
MAX_EMBEDDING_DIM = 4096  # maximum supported embeding size - do NOT change or else DBs will need to be reset
DEFAULT_EMBEDDING_CHUNK_SIZE = 300
# Function return limits
FUNCTION_RETURN_CHAR_LIMIT = 3000  # ~300 words

COMPOSIO_TOOL_TAG_NAME = "composio"

LUANN_CORE_TOOL_MODULE_NAME = "luann.functions.function_sets.base"
LUANN_MULTI_AGENT_TOOL_MODULE_NAME = "luann.functions.function_sets.multi_agent"
MAX_PAUSE_HEARTBEATS = 360  # in min

MESSAGE_CHATGPT_FUNCTION_MODEL = "gpt-3.5-turbo"
MESSAGE_CHATGPT_FUNCTION_SYSTEM_MESSAGE = "You are a helpful assistant. Keep your responses short and concise."

#### Functions related

# REQ_HEARTBEAT_MESSAGE = f"{NON_USER_MSG_PREFIX}request_heartbeat == true"
REQ_HEARTBEAT_MESSAGE = f"{NON_USER_MSG_PREFIX}Function called using request_heartbeat=true, returning control"
# FUNC_FAILED_HEARTBEAT_MESSAGE = f"{NON_USER_MSG_PREFIX}Function call failed"
FUNC_FAILED_HEARTBEAT_MESSAGE = f"{NON_USER_MSG_PREFIX}Function call failed, returning control"

FUNCTION_PARAM_NAME_REQ_HEARTBEAT = "request_heartbeat"
FUNCTION_PARAM_TYPE_REQ_HEARTBEAT = "boolean"
FUNCTION_PARAM_DESCRIPTION_REQ_HEARTBEAT = "Request an immediate heartbeat after function execution. Set to 'true' if you want to send a follow-up message or run a follow-up function."

RETRIEVAL_QUERY_DEFAULT_PAGE_SIZE = 5

# GLOBAL SETTINGS FOR `json.dumps()`
JSON_ENSURE_ASCII = False

# GLOBAL SETTINGS FOR `json.loads()`
JSON_LOADS_STRICT = False
