
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from luann.local_llm.constants import DEFAULT_WRAPPER_NAME
class ToolSettings(BaseSettings):
    # composio_api_key: Optional[str] = None
    # E2B Sandbox configurations
    e2b_api_key: Optional[str] = None
    e2b_sandbox_template_id: Optional[str] = None  # Updated manually

    # Local Sandbox configurations
    local_sandbox_dir: Optional[str] = None
class SummarizerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="luann_summarizer_", extra="ignore")

    # Controls if we should evict all messages
    # TODO: Can refactor this into an enum if we have a bunch of different kinds of summarizers
    evict_all_messages: bool = False

    # The maximum number of retries for the summarizer
    # If we reach this cutoff, it probably means that the summarizer is not compressing down the in-context messages any further
    # And we throw a fatal error
    max_summarizer_retries: int = 3

    # When to warn the model that a summarize command will happen soon
    # The amount of tokens before a system warning about upcoming truncation is sent to Luann
    memory_warning_threshold: float = 0.75

    # Whether to send the system memory warning message
    send_memory_warning_message: bool = False

    # The desired memory pressure to summarize down to
    desired_memory_token_pressure: float = 0.3

    # The number of messages at the end to keep
    # Even when summarizing, we may want to keep a handful of recent messages
    # These serve as in-context examples of how to use functions / what user messages look like
    keep_last_n_messages: int = 0
class ModelSettings(BaseSettings):

    # env_prefix='my_prefix_'

    # when we use /completions APIs (instead of /chat/completions), we need to specify a model wrapper
    # the "model wrapper" is responsible for prompt formatting and function calling parsing
    default_prompt_formatter: str = DEFAULT_WRAPPER_NAME

    # openai
    openai_api_key: Optional[str] = None
    openai_api_base: str = "https://api.openai.com/v1"

    # # groq
    # groq_api_key: Optional[str] = None

    # anthropic
    anthropic_api_key: Optional[str] = None

    # ollama
    ollama_base_url: Optional[str] = None
   # Bedrock
    aws_access_key: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None
    # bedrock_anthropic_version: Optional[str] = "bedrock-2023-05-31"

    # azure
    azure_api_key: Optional[str] = None
    azure_base_url: Optional[str] = None
    # We provide a default here, since usually people will want to be on the latest API version.
    azure_api_version: Optional[str] = (
        "2024-09-01-preview"  # https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation
    )

    # google ai
    gemini_api_key: Optional[str] = None
    # # together
    # together_api_key: Optional[str] = None
    # vLLM
    vllm_api_base: Optional[str] = None

    # openllm
    openllm_auth_type: Optional[str] = None
    openllm_api_key: Optional[str] = None

     # disable openapi schema generation
    disable_schema_generation: bool = False



cors_origins = [
    "http://luann.localhost",
    "http://localhost:8283",
    "http://localhost:8083",
    "http://localhost:3000",
    "http://localhost:4200",
]
# read pg_uri from luann.~/uann/pg_uri or set to none, this is to support Luann Desktop
default_pg_uri = None

## check if --use-file-pg-uri is passed
import sys

if "--use-file-pg-uri" in sys.argv:
    try:
        with open(Path.home() / ".luann/pg_uri", "r") as f:
            default_pg_uri = f.read()
            print("Read pg_uri from luann.~/.luann/pg_uri")
    except FileNotFoundError:
        pass

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="luann_")

    luann_dir: Optional[Path] = Field(Path.home() / ".luann", env="LUANN_DIR")
    debug: Optional[bool] = False
    cors_origins: Optional[list] = cors_origins

    # database configuration
    pg_db: Optional[str] = None
    pg_user: Optional[str] = None
    pg_password: Optional[str] = None
    pg_host: Optional[str] = None
    pg_port: Optional[int] = None
    pg_uri: Optional[str] = None  # option to specifiy full uri
    pg_pool_size: int = 20  # Concurrent connections
    pg_max_overflow: int = 10  # Overflow limit
    pg_pool_timeout: int = 30  # Seconds to wait for a connection
    pg_pool_recycle: int = 1800  # When to recycle connections
    pg_echo: bool = False  # Logging
    # tools configuration
    load_default_external_tools: Optional[bool] = None

    @property
    def luann_pg_uri(self) -> str:
        if self.pg_uri:
            return self.pg_uri
        elif self.pg_db and self.pg_user and self.pg_password and self.pg_host and self.pg_port:
            return f"postgresql+pg8000://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        else:
            return f"postgresql+pg8000://luann:luann@localhost:5432/luann"

    # add this property to avoid being returned the default
    # reference: https://github.com/cpacker/Luann/issues/1362
    @property
    def luann_pg_uri_no_default(self) -> str:
        if self.pg_uri:
            return self.pg_uri
        elif self.pg_db and self.pg_user and self.pg_password and self.pg_host and self.pg_port:
            return f"postgresql+pg8000://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        else:
            return None


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_prefix="luann_test_")

    luann_dir: Optional[Path] = Field(Path.home() / ".luann/test", env="LUANN_TEST_DIR")


# singleton
settings = Settings(_env_parse_none_str="None")
# settings.pg_uri="postgresql+psycopg2://postgres:864791@localhost:5432/postgres"
# test_settings = TestSettings()
# model_settings = ModelSettings()
tool_settings = ToolSettings()
summarizer_settings = SummarizerSettings()
