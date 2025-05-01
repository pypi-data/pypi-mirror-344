# import local_llm.llm_chat_completion_wrappers.airoboros as airoboros
from luann.local_llm.llm_chat_completion_wrappers.chatml import (
    ChatMLInnerMonologueWrapper,
)



# DEFAULT_OLLAMA_MODEL = "dolphin2.2-mistral:7b-q6_K"

# DEFAULT_WRAPPER = airoboros.Airoboros21InnerMonologueWrapper
# DEFAULT_WRAPPER_NAME = "airoboros-l2-70b-2.1"

DEFAULT_WRAPPER = ChatMLInnerMonologueWrapper
DEFAULT_WRAPPER_NAME = "chatml"

INNER_THOUGHTS_KWARG = "inner_thoughts"
INNER_THOUGHTS_KWARG_DESCRIPTION = "Deep inner monologue private to you only."
INNER_THOUGHTS_KWARG_DESCRIPTION_GO_FIRST = f"Deep inner monologue private to you only. Think before you act, so always generate arg '{INNER_THOUGHTS_KWARG}' first before any other arg."
INNER_THOUGHTS_CLI_SYMBOL = "💭"

ASSISTANT_MESSAGE_CLI_SYMBOL = "🤖"
