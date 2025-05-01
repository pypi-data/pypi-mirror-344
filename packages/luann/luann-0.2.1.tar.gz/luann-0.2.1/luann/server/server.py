# inspecting tools
import asyncio
import os
import traceback
import warnings
from abc import abstractmethod
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple, Union


from fastapi import HTTPException
from fastapi.responses import StreamingResponse

import luann.constants as constants
import luann.server.utils as server_utils
import luann.system as system
from luann.agent import Agent, save_agent

from luann.data_sources.connectors import DataConnector, load_data

# TODO use custom interface
from luann.interface import AgentInterface  # abstract
from luann.interface import CLIInterface  # for printing to terminal
from luann.log import get_logger
# from luann.offline_memory_agent import OfflineMemoryAgent
from luann.orm import Base
from luann.orm.errors import NoResultFound
from luann.schemas.agent import AgentState, AgentType, CreateAgent
from luann.schemas.block import BlockUpdate
from luann.schemas.embedding_config import EmbeddingConfig

# openai schemas
from luann.schemas.enums import JobStatus, MessageStreamStatus
from luann.schemas.environment_variables import SandboxEnvironmentVariableCreate
from luann.schemas.job import Job, JobUpdate
from luann.schemas.luann_message import LegacyLuannMessage, LuannMessage, ToolReturnMessage
from luann.schemas.luann_response import LuannResponse
from luann.schemas.llm_config import LLMConfig
from luann.schemas.memory import ArchivalMemorySummary, ContextWindowOverview, Memory, RecallMemorySummary
from luann.schemas.message import Message, MessageCreate, MessageRole, MessageUpdate,TextContent
from luann.schemas.organization import Organization
from luann.schemas.passage import Passage
from luann.schemas.source import Source as PydanticSource
from luann.schemas.source import SourceCreate
from luann.schemas.providers import (
    AnthropicProvider,
    AzureProvider,
    GoogleAIProvider,
    # GroqProvider,
    LuannProvider,
    OllamaProvider,
    OpenAIProvider,
    Provider,
    # TogetherProvider,
    VLLMChatCompletionsProvider,
    VLLMCompletionsProvider,

)
from luann.schemas.sandbox_config import SandboxType
from luann.schemas.source import Source
from luann.schemas.tool import Tool
from luann.schemas.usage import LuannUsageStatistics
from luann.schemas.user import User
from luann.server.rest_api.chat_completions_interface import ChatCompletionsStreamingInterface
from luann.server.rest_api.interface import StreamingServerInterface
from luann.server.rest_api.utils import sse_async_generator
from luann.services.agent_manager import AgentManager
from luann.services.block_manager import BlockManager
from luann.services.job_manager import JobManager
from luann.services.message_manager import MessageManager
from luann.services.organization_manager import OrganizationManager
from luann.services.passage_manager import PassageManager
# from luann.services.per_agent_lock_manager import PerAgentLockManager
from luann.services.provider_manager import ProviderManager
from luann.services.sandbox_config_manager import SandboxConfigManager
from luann.services.source_manager import SourceManager
# from luann.services.step_manager import StepManager
from luann.services.tool_execution_sandbox import ToolExecutionSandbox
from luann.services.tool_manager import ToolManager
from luann.services.user_manager import UserManager
from luann.utils import get_friendly_error_msg, get_utc_time, json_dumps, json_loads

logger = get_logger(__name__)


class Server(object):
    """Abstract server class that supports multi-agent multi-user"""

    @abstractmethod
    def list_agents(self, user_id: str) -> dict:
        """List all available agents to a user"""
        raise NotImplementedError

    @abstractmethod
    def get_agent_memory(self, user_id: str, agent_id: str) -> dict:
        """Return the memory of an agent (core memory + non-core statistics)"""
        raise NotImplementedError

    @abstractmethod
    def get_server_config(self, user_id: str) -> dict:
        """Return the base config"""
        raise NotImplementedError

    @abstractmethod
    def update_agent_core_memory(self, user_id: str, agent_id: str, label: str, actor: User) -> Memory:
        """Update the agents core memory block, return the new state"""
        raise NotImplementedError

    @abstractmethod
    def create_agent(
        self,
        request: CreateAgent,
        actor: User,
        # interface
        interface: Union[AgentInterface, None] = None,
    ) -> AgentState:
        """Create a new agent using a config"""
        raise NotImplementedError

    @abstractmethod
    def user_message(self, user_id: str, agent_id: str, message: str) -> None:
        """Process a message from luann.the user, internally calls step"""
        raise NotImplementedError

    @abstractmethod
    def system_message(self, user_id: str, agent_id: str, message: str) -> None:
        """Process a message from luann.the system, internally calls step"""
        raise NotImplementedError

    @abstractmethod
    def send_messages(self, user_id: str, agent_id: str, messages: Union[MessageCreate, List[Message]]) -> None:
        """Send a list of messages to the agent"""
        raise NotImplementedError

    @abstractmethod
    def run_command(self, user_id: str, agent_id: str, command: str) -> Union[str, None]:
        """Run a command on the agent, e.g. /memory

        May return a string with a message generated by the command
        """
        raise NotImplementedError


from contextlib import contextmanager

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from luann.config import LuannConfig

# NOTE: hack to see if single session management works
from luann.settings import  settings, tool_settings

config = LuannConfig.load()


def print_sqlite_schema_error():
    """Print a formatted error message for SQLite schema issues"""
    console = Console()
    error_text = Text()
    error_text.append("Existing SQLite DB schema is invalid, and schema migrations are not supported for SQLite. ", style="bold red")
    error_text.append("To have migrations supported between luann versions, please run Luann with Docker (", style="white")
    error_text.append("https://docs.luann.com/server/docker", style="blue underline")
    error_text.append(") or use Postgres by setting ", style="white")
    error_text.append("luann_PG_URI", style="yellow")
    error_text.append(".\n\n", style="white")
    error_text.append("If you wish to keep using SQLite, you can reset your database by removing the DB file with ", style="white")
    error_text.append("rm ~/.luann/sqlite.db", style="yellow")
    error_text.append(" or downgrade to your previous version of luann.", style="white")

    console.print(Panel(error_text, border_style="red"))


@contextmanager
def db_error_handler():
    """Context manager for handling database errors"""
    try:
        yield
    except Exception as e:
        # Handle other SQLAlchemy errors
        print(e)
        print_sqlite_schema_error()
        # raise ValueError(f"SQLite DB error: {str(e)}")
        exit(1)


# print("Creating engine", settings.luann_pg_uri)
if settings.luann_pg_uri_no_default:
    print("Creating engine", settings.luann_pg_uri)
    config.recall_storage_type = "postgres"
    config.recall_storage_uri = settings.luann_pg_uri_no_default
    config.archival_storage_type = "postgres"
    config.archival_storage_uri = settings.luann_pg_uri_no_default

    # create engine
    # print("Creating engine stat:::::::::::::::::::::::::::::", settings.luann_pg_uri)
    engine = create_engine(
        settings.luann_pg_uri,
        pool_size=settings.pg_pool_size,
        max_overflow=settings.pg_max_overflow,
        pool_timeout=settings.pg_pool_timeout,
        pool_recycle=settings.pg_pool_recycle,
        echo=settings.pg_echo,
    )

    Base.metadata.create_all(bind=engine)
else:
    
    sqliteurl="sqlite:///" + os.path.join(config.recall_storage_path, "sqlite.db")

    print("Creating engine", sqliteurl)
    # TODO: don't rely on config storage
    engine = create_engine(sqliteurl)

    # Store the original connect method
    original_connect = engine.connect

    def wrapped_connect(*args, **kwargs):
        with db_error_handler():
            # Get the connection
            connection = original_connect(*args, **kwargs)

            # Store the original execution method
            original_execute = connection.execute

            # Wrap the execute method of the connection
            def wrapped_execute(*args, **kwargs):
                with db_error_handler():
                    return original_execute(*args, **kwargs)

            # Replace the connection's execute method
            connection.execute = wrapped_execute

            return connection

    # Replace the engine's connect method
    engine.connect = wrapped_connect

    Base.metadata.create_all(bind=engine)


# print(f"engine:{engine}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from contextlib import contextmanager

db_context = contextmanager(get_db)


class SyncServer(Server):
    """Simple single-threaded / blocking server process"""

    def __init__(
        self,
        chaining: bool = True,
        max_chaining_steps: Optional[bool] = None,
        default_interface_factory: Callable[[], AgentInterface] = lambda: CLIInterface(),
        init_with_default_org_and_user: bool = True,
        # default_interface: AgentInterface = CLIInterface(),
        # default_persistence_manager_cls: PersistenceManager = LocalStateManager,
        # auth_mode: str = "none",  # "none, "jwt", "external"
    ):
        """Server process holds in-memory agents that are being run"""
        # chaining = whether or not to run again if request_heartbeat=true
        self.chaining = chaining

        # if chaining == true, what's the max number of times we'll chain before yielding?
        # none = no limit, can go on forever
        self.max_chaining_steps = max_chaining_steps

        # The default interface that will get assigned to agents ON LOAD
        self.default_interface_factory = default_interface_factory

       

        # Initialize the metadata store
        config = LuannConfig.load()
        if settings.luann_pg_uri_no_default:
            config.recall_storage_type = "postgres"
            config.recall_storage_uri = settings.luann_pg_uri_no_default
            config.archival_storage_type = "postgres"
            config.archival_storage_uri = settings.luann_pg_uri_no_default
        config.save()
        self.config = config

        # Managers that interface with data models
        self.organization_manager = OrganizationManager()
        self.passage_manager = PassageManager()
        self.user_manager = UserManager()
        self.tool_manager = ToolManager()
        self.block_manager = BlockManager()
        self.source_manager = SourceManager()
        self.sandbox_config_manager = SandboxConfigManager(tool_settings)
        self.message_manager = MessageManager()
        self.job_manager = JobManager()
        self.agent_manager = AgentManager()
        self.provider_manager = ProviderManager()
        # self.step_manager = StepManager()
        # Managers that interface with parallelism
        # self.per_agent_lock_manager = PerAgentLockManager()

        # Make default user and org
        if init_with_default_org_and_user:
            self.default_org = self.organization_manager.create_default_organization()
            self.default_user = self.user_manager.create_default_user()
            self.block_manager.add_default_blocks(actor=self.default_user)
            self.tool_manager.upsert_base_tools(actor=self.default_user)

           
    def enabled_real_provider_from_db(self,actor: User):
        temp_real_provider: List[Provider] = [LuannProvider()]
        # temp_real_provider=[]
        list_enabled_providers_from_db=self.provider_manager.list_providers(actor=actor)
        if len(list_enabled_providers_from_db)>0:
           for enabled_provoder in list_enabled_providers_from_db:
               if enabled_provoder.is_enabled==True:
                    if enabled_provoder.name=="azure":
                       temp_real_provider.append(
                               AzureProvider(
                                 api_key=enabled_provoder.api_key,
                                 base_url=enabled_provoder.base_url,
                                 api_version=enabled_provoder.api_version,
                                           )
                            )
                    if enabled_provoder.name=="openai":
                       temp_real_provider.append(
                               OpenAIProvider(
                                api_key=enabled_provoder.api_key,
                                base_url=enabled_provoder.base_url,
                                           )
                            )
                    if enabled_provoder.name=="openai":
                       temp_real_provider.append(
                               OpenAIProvider(
                                api_key=enabled_provoder.api_key,
                                base_url=enabled_provoder.base_url,
                                           )
                            )
                       
                    if enabled_provoder.name=="anthropic":
                       temp_real_provider.append(
                               AnthropicProvider(
                                api_key=enabled_provoder.api_key,
                               
                                           )
                            )
                    if enabled_provoder.name=="google_ai":
                       temp_real_provider.append(
                               GoogleAIProvider(
                                api_key=enabled_provoder.api_key,
                               
                                           )
                            )
                    if enabled_provoder.name=="ollama":
                       temp_real_provider.append(
                               OllamaProvider(
                                api_key=enabled_provoder.api_key,
                                base_url=enabled_provoder.base_url,
                                default_prompt_formatter=enabled_provoder.default_prompt_formatter,
                               
                                           )
                            )
                   
                    if enabled_provoder.name=="vllm":
                       temp_real_provider.append(
                               VLLMCompletionsProvider(
                               
                                base_url=enabled_provoder.base_url,
                                default_prompt_formatter=enabled_provoder.default_prompt_formatter,
                               
                                           )
                            )
        return temp_real_provider
    def load_agent(self, agent_id: str, actor: User, interface: Union[AgentInterface, None] = None) -> Agent:
            """Updated method to load agents from luann.persisted storage"""
            # agent_lock = self.per_agent_lock_manager.get_lock(agent_id)
            # print(f"agent_lock:{agent_lock}")
            # with agent_lock:
            agent_state = self.agent_manager.get_agent_by_id(agent_id=agent_id, actor=actor)
            # print(f"agent_state:{agent_state}")

            interface = interface or self.default_interface_factory()
            if agent_state.agent_type == AgentType.memgpt_agent:
                agent = Agent(agent_state=agent_state, interface=interface, user=actor)
            # elif agent_state.agent_type == AgentType.offline_memory_agent:
            #     agent = OfflineMemoryAgent(agent_state=agent_state, interface=interface, user=actor)
            # elif agent_state.agent_type == AgentType.chat_only_agent:
            #     agent = ChatOnlyAgent(agent_state=agent_state, interface=interface, user=actor)
            else:
                raise ValueError(f"Invalid agent type {agent_state.agent_type}")

            return agent

    def _step(
        self,
        actor: User,
        agent_id: str,
        input_messages: Union[Message, List[Message]],
        interface: Union[AgentInterface, None] = None,  # needed to getting responses
        # timestamp: Optional[datetime],
    ) -> LuannUsageStatistics:
        """Send the input message through the agent"""
        # TODO: Thread actor directly through this function, since the top level caller most likely already retrieved the user
        # Input validation
        if isinstance(input_messages, Message):
            input_messages = [input_messages]
        if not all(isinstance(m, Message) for m in input_messages):
            raise ValueError(f"messages should be a Message or a list of Message, got {type(input_messages)}")

        logger.debug(f"Got input messages: {input_messages}")
        luann_agent = None
        try:
            luann_agent = self.load_agent(agent_id=agent_id, interface=interface, actor=actor)
            if luann_agent is None:
                raise KeyError(f"Agent (user={actor.id}, agent={agent_id}) is not loaded")

            # Determine whether or not to token stream based on the capability of the interface
            token_streaming = luann_agent.interface.streaming_mode if hasattr(luann_agent.interface, "streaming_mode") else False

            logger.debug(f"Starting agent step")
            if interface:
                metadata = interface.metadata if hasattr(interface, "metadata") else None
            else:
                metadata = None
            usage_stats = luann_agent.step(
                messages=input_messages,
                chaining=self.chaining,
                max_chaining_steps=self.max_chaining_steps,
                stream=token_streaming,
                skip_verify=True,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error in server._step: {e}")
            print(traceback.print_exc())
            raise
        finally:
            logger.debug("Calling step_yield()")
            if luann_agent:
                luann_agent.interface.step_yield()

        return usage_stats



    def user_message(
        self,
        user_id: str,
        agent_id: str,
        message: Union[str, Message],
        timestamp: Optional[datetime] = None,
    ) -> LuannUsageStatistics:
        """Process an incoming user message and feed it through the luann agent"""
        try:
            actor = self.user_manager.get_user_by_id(user_id=user_id)
        except NoResultFound:
            raise ValueError(f"User user_id={user_id} does not exist")

        try:
            agent = self.agent_manager.get_agent_by_id(agent_id=agent_id, actor=actor)
        except NoResultFound:
            raise ValueError(f"Agent agent_id={agent_id} does not exist")

        # Basic input sanitization
        if isinstance(message, str):
            if len(message) == 0:
                raise ValueError(f"Invalid input: '{message}'")

            # If the input begins with a command prefix, reject
            elif message.startswith("/"):
                raise ValueError(f"Invalid input: '{message}'")

            packaged_user_message = system.package_user_message(
                user_message=message,
                time=timestamp.isoformat() if timestamp else None,
            )

            # NOTE: eventually deprecate and only allow passing Message types
            # Convert to a Message object
            if timestamp:
                message = Message(
                    agent_id=agent_id,
                    role="user",
                    text=packaged_user_message,
                    created_at=timestamp,
                )
            else:
                message = Message(
                    agent_id=agent_id,
                    role="user",
                    text=packaged_user_message,
                )

        # Run the agent state forward
        usage = self._step(actor=actor, agent_id=agent_id, input_messages=message)
        return usage

    def system_message(
        self,
        user_id: str,
        agent_id: str,
        message: Union[str, Message],
        timestamp: Optional[datetime] = None,
    ) -> LuannUsageStatistics:
        """Process an incoming system message and feed it through the luann agent"""
        try:
            actor = self.user_manager.get_user_by_id(user_id=user_id)
        except NoResultFound:
            raise ValueError(f"User user_id={user_id} does not exist")

        try:
            agent = self.agent_manager.get_agent_by_id(agent_id=agent_id, actor=actor)
        except NoResultFound:
            raise ValueError(f"Agent agent_id={agent_id} does not exist")

        # Basic input sanitization
        if isinstance(message, str):
            if len(message) == 0:
                raise ValueError(f"Invalid input: '{message}'")

            # If the input begins with a command prefix, reject
            elif message.startswith("/"):
                raise ValueError(f"Invalid input: '{message}'")

            packaged_system_message = system.package_system_message(system_message=message)

            # NOTE: eventually deprecate and only allow passing Message types
            # Convert to a Message object

            if timestamp:
                message = Message(
                    agent_id=agent_id,
                    role="system",
                    text=packaged_system_message,
                    created_at=timestamp,
                )
            else:
                message = Message(
                    agent_id=agent_id,
                    role="system",
                    text=packaged_system_message,
                )

        if isinstance(message, Message):
            # Can't have a null text field
            if message.text is None or len(message.text) == 0:
                raise ValueError(f"Invalid input: '{message.text}'")
            # If the input begins with a command prefix, reject
            elif message.text.startswith("/"):
                raise ValueError(f"Invalid input: '{message.text}'")

        else:
            raise TypeError(f"Invalid input: '{message}' - type {type(message)}")

        if timestamp:
            # Override the timestamp with what the caller provided
            message.created_at = timestamp

        # Run the agent state forward
        return self._step(actor=actor, agent_id=agent_id, input_messages=message)

    def send_messages(
        self,
        actor: User,
        agent_id: str,
        messages: Union[List[MessageCreate], List[Message]],
        # whether or not to wrap user and system message as MemGPT-style stringified JSON
        wrap_user_message: bool = True,
        wrap_system_message: bool = True,
        interface: Union[AgentInterface, ChatCompletionsStreamingInterface, None] = None,  # needed to getting responses
        metadata: Optional[dict] = None,  # Pass through metadata to interface
    ) -> LuannUsageStatistics:
        """Send a list of messages to the agent

        If the messages are of type MessageCreate, we need to turn them into
        Message objects first before sending them through step.

        Otherwise, we can pass them in directly.
        """
        message_objects: List[Message] = []

        if all(isinstance(m, MessageCreate) for m in messages):
            for message in messages:
                assert isinstance(message, MessageCreate)

                # If wrapping is enabled, wrap with metadata before placing content inside the Message object
                if message.role == MessageRole.user and wrap_user_message:
                    message.content = system.package_user_message(user_message=message.content)
                elif message.role == MessageRole.system and wrap_system_message:
                    message.content = system.package_system_message(system_message=message.content)
                else:
                    raise ValueError(f"Invalid message role: {message.role}")


                # print(f"message.content:{message.content}")
                # Create the Message object
                message_objects.append(
                    Message(
                        agent_id=agent_id,
                        role=message.role,
                        content=[TextContent(text=str(message.content))],
                        name=message.name,
                        # assigned later?
                        model=None,
                        # irrelevant
                        tool_calls=None,
                        tool_call_id=None,
                    )
                )

        elif all(isinstance(m, Message) for m in messages):
            for message in messages:
                assert isinstance(message, Message)
                message_objects.append(message)

        else:
            raise ValueError(f"All messages must be of type Message or MessageCreate, got {[type(message) for message in messages]}")

        # Store metadata in interface if provided
        if metadata and hasattr(interface, "metadata"):
            interface.metadata = metadata

        # Run the agent state forward
        return self._step(actor=actor, agent_id=agent_id, input_messages=message_objects, interface=interface)


  

    def create_source(
        self,
        request: SourceCreate,
        actor: User,
        # interface
    ) -> PydanticSource:
        
        if request.embedding_config is None:
            if request.embedding is None:
                raise ValueError("Must specify either embedding or embedding_config in request")
            request.embedding_config = self.get_embedding_config_from_handle(
                actor=actor,handle=request.embedding, embedding_chunk_size=request.embedding_chunk_size or constants.DEFAULT_EMBEDDING_CHUNK_SIZE
            )

            print(request.embedding_config)

        """Create a new agent using a config"""
        # Invoke manager
        return self.source_manager.create_source(
            source=PydanticSource(
                name=request.name,
                description=request.description,
                embedding_config=request.embedding_config,
                metadata_=request.metadata_,

            ),
            actor=actor,
        )
    


    def create_agent(
        self,
        request: CreateAgent,
        actor: User,
        # interface
        interface: Union[AgentInterface, None] = None,
    ) -> AgentState:
        if request.llm_config is None:
            if request.llm is None:
                raise ValueError("Must specify either llm or llm_config in request")
            request.llm_config = self.get_llm_config_from_handle(actor=actor,handle=request.llm, context_window_limit=request.context_window_limit)

        if request.embedding_config is None:
            if request.embedding is None:
                raise ValueError("Must specify either embedding or embedding_config in request")
            request.embedding_config = self.get_embedding_config_from_handle(
                actor=actor,handle=request.embedding, embedding_chunk_size=request.embedding_chunk_size or constants.DEFAULT_EMBEDDING_CHUNK_SIZE
            )

        """Create a new agent using a config"""
        # Invoke manager
        return self.agent_manager.create_agent(
            agent_create=request,
            actor=actor,
        )

    # convert name->id

    # TODO: These can be moved to agent_manager
    def get_agent_memory(self, agent_id: str, actor: User) -> Memory:
        """Return the memory of an agent (core memory)"""
        return self.agent_manager.get_agent_by_id(agent_id=agent_id, actor=actor).memory

    def get_archival_memory_summary(self, agent_id: str, actor: User) -> ArchivalMemorySummary:
        return ArchivalMemorySummary(size=self.agent_manager.passage_size(actor=actor, agent_id=agent_id))

    def get_recall_memory_summary(self, agent_id: str, actor: User) -> RecallMemorySummary:
        return RecallMemorySummary(size=self.message_manager.size(actor=actor, agent_id=agent_id))

    def get_agent_archival(
        self,
        user_id: str,
        agent_id: str,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[int] = 100,
        order_by: Optional[str] = "created_at",
        reverse: Optional[bool] = False,
    ) -> List[Passage]:
        # TODO: Thread actor directly through this function, since the top level caller most likely already retrieved the user
        actor = self.user_manager.get_user_or_default(user_id=user_id)

        # iterate over records
        records = self.agent_manager.list_passages(
            actor=actor,
            agent_id=agent_id,
            after=after,
            before=before,
            limit=limit,
            ascending=not reverse,
        )
        return records

   

    def insert_archival_memory(self, agent_id: str, memory_contents: str, actor: User) -> List[Passage]:
        # Get the agent object (loaded in memory)
        agent_state = self.agent_manager.get_agent_by_id(agent_id=agent_id, actor=actor)
        # Insert into archival memory
        # TODO: @mindy look at moving this to agent_manager to avoid above extra call
        passages = self.passage_manager.insert_passage(agent_state=agent_state, agent_id=agent_id, text=memory_contents, actor=actor)

        return passages

    def delete_archival_memory(self, memory_id: str, actor: User):
        # TODO check if it exists first, and throw error if not
        # TODO: @mindy make this return the deleted passage instead
        self.passage_manager.delete_passage_by_id(passage_id=memory_id, actor=actor)

        # TODO: return archival memory

    def get_agent_recall(
        self,
        user_id: str,
        agent_id: str,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[int] = 100,
        reverse: Optional[bool] = False,
        return_message_object: bool = True,
        use_assistant_message: bool = True,
        assistant_message_tool_name: str = constants.DEFAULT_MESSAGE_TOOL,
        assistant_message_tool_kwarg: str = constants.DEFAULT_MESSAGE_TOOL_KWARG,
    ) -> Union[List[Message], List[LuannMessage]]:
        # TODO: Thread actor directly through this function, since the top level caller most likely already retrieved the user

        actor = self.user_manager.get_user_or_default(user_id=user_id)
        start_date = self.message_manager.get_message_by_id(after, actor=actor).created_at if after else None
        end_date = self.message_manager.get_message_by_id(before, actor=actor).created_at if before else None

        records = self.message_manager.list_messages_for_agent(
            agent_id=agent_id,
            actor=actor,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            ascending=not reverse,
        )

        if not return_message_object:
            records = Message.to_luann_messages_from_list(
                messages=records,
                use_assistant_message=use_assistant_message,
                assistant_message_tool_name=assistant_message_tool_name,
                assistant_message_tool_kwarg=assistant_message_tool_kwarg,
            )

        if reverse:
            records = records[::-1]

        return records

    def get_server_config(self, include_defaults: bool = False) -> dict:
        """Return the base config"""

        def clean_keys(config):
            config_copy = config.copy()
            for k, v in config.items():
                if k == "key" or "_key" in k:
                    config_copy[k] = server_utils.shorten_key_middle(v, chars_each_side=5)
            return config_copy

        # TODO: do we need a separate server config?
        base_config = vars(self.config)
        clean_base_config = clean_keys(base_config)

        response = {"config": clean_base_config}

        if include_defaults:
            default_config = vars(LuannConfig())
            clean_default_config = clean_keys(default_config)
            response["defaults"] = clean_default_config

        return response

    def get_server_config(self, include_defaults: bool = False) -> dict:
        """Return the base config"""

        def clean_keys(config):
            config_copy = config.copy()
            for k, v in config.items():
                if k == "key" or "_key" in k:
                    config_copy[k] = server_utils.shorten_key_middle(v, chars_each_side=5)
            return config_copy

        # TODO: do we need a separate server config?
        base_config = vars(self.config)
        clean_base_config = clean_keys(base_config)

        response = {"config": clean_base_config}

        if include_defaults:
            default_config = vars(LuannConfig())
            clean_default_config = clean_keys(default_config)
            response["defaults"] = clean_default_config

        return response

    def update_agent_core_memory(self, agent_id: str, label: str, value: str, actor: User) -> Memory:
        """Update the value of a block in the agent's memory"""

        # get the block id
        block = self.agent_manager.get_block_with_label(agent_id=agent_id, block_label=label, actor=actor)

        # update the block
        self.block_manager.update_block(block_id=block.id, block_update=BlockUpdate(value=value), actor=actor)

        # rebuild system prompt for agent, potentially changed
        return self.agent_manager.rebuild_system_prompt(agent_id=agent_id, actor=actor).memory

    def delete_source(self, source_id: str, actor: User):
        """Delete a data source"""
        self.source_manager.delete_source(source_id=source_id, actor=actor)

        # delete data from luann.passage store
        passages_to_be_deleted = self.agent_manager.list_passages(actor=actor, source_id=source_id, limit=None)
        self.passage_manager.delete_passages(actor=actor, passages=passages_to_be_deleted)

        # TODO: delete data from luann.agent passage stores (?)

    def load_file_to_source(self, source_id: str, file_path: str, job_id: str, actor: User) -> Job:

        # update job
        job = self.job_manager.get_job_by_id(job_id, actor=actor)
        job.status = JobStatus.running
        self.job_manager.update_job_by_id(job_id=job_id, job_update=JobUpdate(**job.model_dump()), actor=actor)

        # try:
        from luann.data_sources.connectors import DirectoryConnector

        source = self.source_manager.get_source_by_id(source_id=source_id)
        if source is None:
            raise ValueError(f"Source {source_id} does not exist")
        connector = DirectoryConnector(input_files=[file_path])
        num_passages, num_documents = self.load_data(user_id=source.created_by_id, source_name=source.name, connector=connector)

        # update job status
        job.status = JobStatus.completed
        job.metadata_["num_passages"] = num_passages
        job.metadata_["num_documents"] = num_documents
        self.job_manager.update_job_by_id(job_id=job_id, job_update=JobUpdate(**job.model_dump()), actor=actor)

        # update all agents who have this source attached
        agent_states = self.source_manager.list_attached_agents(source_id=source_id, actor=actor)
        for agent_state in agent_states:
            agent_id = agent_state.id

            # Attach source to agent
            curr_passage_size = self.agent_manager.passage_size(actor=actor, agent_id=agent_id)
            self.agent_manager.attach_source(agent_id=agent_state.id, source_id=source_id, actor=actor)
            new_passage_size = self.agent_manager.passage_size(actor=actor, agent_id=agent_id)
            assert new_passage_size >= curr_passage_size  # in case empty files are added

        return job

    def load_data(
        self,
        user_id: str,
        connector: DataConnector,
        source_name: str,
    ) -> Tuple[int, int]:
        """Load data from luann.a DataConnector into a source for a specified user_id"""
        # TODO: this should be implemented as a batch job or at least async, since it may take a long time

        # load data from luann.a data source into the document store
        user = self.user_manager.get_user_by_id(user_id=user_id)
        source = self.source_manager.get_source_by_name(source_name=source_name, actor=user)
        if source is None:
            raise ValueError(f"Data source {source_name} does not exist for user {user_id}")

        # load data into the document store
        passage_count, document_count = load_data(connector, source, self.passage_manager, self.source_manager, actor=user)
        return passage_count, document_count

    def list_data_source_passages(self, user_id: str, source_id: str) -> List[Passage]:
        warnings.warn("list_data_source_passages is not yet implemented, returning empty list.", category=UserWarning)
        return []

    def list_all_sources(self, actor: User) -> List[Source]:
        """List all sources (w/ extra metadata) belonging to a user"""

        sources = self.source_manager.list_sources(actor=actor)

        # Add extra metadata to the sources
        sources_with_metadata = []
        for source in sources:

            # count number of passages
            num_passages = self.agent_manager.passage_size(actor=actor, source_id=source.id)

            # TODO: add when files table implemented
            ## count number of files
            # document_conn = StorageConnector.get_storage_connector(TableType.FILES, self.config, user_id=user_id)
            # num_documents = document_conn.size({"data_source": source.name})
            num_documents = 0

            agents = self.source_manager.list_attached_agents(source_id=source.id, actor=actor)
            # add the agent name information
            attached_agents = [{"id": agent.id, "name": agent.name} for agent in agents]

            # Overwrite metadata field, should be empty anyways
            source.metadata_ = dict(
                num_documents=num_documents,
                num_passages=num_passages,
                attached_agents=attached_agents,
            )

            sources_with_metadata.append(source)

        return sources_with_metadata

    def update_agent_message(self, message_id: str, request: MessageUpdate, actor: User) -> Message:
        """Update the details of a message associated with an agent"""

        # Get the current message
        return self.message_manager.update_message_by_id(message_id=message_id, message_update=request, actor=actor)

    def get_organization_or_default(self, org_id: Optional[str]) -> Organization:
        """Get the organization object for org_id if it exists, otherwise return the default organization object"""
        if org_id is None:
            org_id = self.organization_manager.DEFAULT_ORG_ID

        try:
            return self.organization_manager.get_organization_by_id(org_id=org_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Organization with id {org_id} not found")

    def list_llm_models(self,actor: User) -> List[LLMConfig]:
        """List available models"""

        llm_models = []
        for provider in self.get_enabled_providers(actor=actor):
            try:
                llm_models.extend(provider.list_llm_models())
            except Exception as e:
                warnings.warn(f"An error occurred while listing LLM models for provider {provider}: {e}")
        return llm_models

    def list_embedding_models(self,actor: User) -> List[EmbeddingConfig]:
        """List available embedding models"""
        embedding_models = []
        for provider in self.get_enabled_providers(actor=actor):
            try:
                embedding_models.extend(provider.list_embedding_models())
            except Exception as e:
                warnings.warn(f"An error occurred while listing embedding models for provider {provider}: {e}")
        return embedding_models

    def get_enabled_providers(self,actor: User):
        
        # providers_from_db = {p.name: p for p in self._enabled_providers}
        # providers_from_db = {p.name: p for p in self.provider_manager.list_providers()}
        providers_from_db_raw= self.enabled_real_provider_from_db(actor=actor)
        providers_from_db={p.name: p for p in providers_from_db_raw}

        # Merge the two dictionaries, keeping the values from luann.providers_from_db where conflicts occur
        return {**providers_from_db}.values()

    def get_llm_config_from_handle(self,actor: User, handle: str, context_window_limit: Optional[int] = None) -> LLMConfig:
        provider_name, model_name = handle.split("/", 1)
        provider = self.get_provider_from_name(provider_name,actor)

        llm_configs = [config for config in provider.list_llm_models() if config.model == model_name]
        # print(f"llm_configs:{llm_configs}")
        if not llm_configs:
            raise ValueError(f"LLM model {model_name} is not supported by {provider_name}")
        elif len(llm_configs) > 1:
            raise ValueError(f"Multiple LLM models with name {model_name} supported by {provider_name}")
        else:
            llm_config = llm_configs[0]

        if context_window_limit:
            if context_window_limit > llm_config.context_window:
                raise ValueError(f"Context window limit ({context_window_limit}) is greater than maximum of ({llm_config.context_window})")
            llm_config.context_window = context_window_limit

        return llm_config

    def get_embedding_config_from_handle(
        self, actor: User,handle: str, embedding_chunk_size: int = constants.DEFAULT_EMBEDDING_CHUNK_SIZE
    ) -> EmbeddingConfig:
        provider_name, model_name = handle.split("/", 1)
        provider = self.get_provider_from_name(provider_name,actor)

        embedding_configs = [config for config in provider.list_embedding_models() if config.embedding_model == model_name]
        if not embedding_configs:
            raise ValueError(f"Embedding model {model_name} is not supported by {provider_name}")
        elif len(embedding_configs) > 1:
            raise ValueError(f"Multiple embedding models with name {model_name} supported by {provider_name}")
        else:
            embedding_config = embedding_configs[0]

        if embedding_chunk_size:
            embedding_config.embedding_chunk_size = embedding_chunk_size
        

        return embedding_config

    def get_provider_from_name(self, provider_name: str,actor: User) -> Provider:
       

        list_enabled_provider=self.enabled_real_provider_from_db(actor=actor)
        providers = [provider for provider in list_enabled_provider if provider.name == provider_name]
        if not providers:
            raise ValueError(f"Provider {provider_name} is not supported")
        elif len(providers) > 1:
            raise ValueError(f"Multiple providers with name {provider_name} supported")
        else:
            provider = providers[0]

        return provider

    def add_llm_model(self, request: LLMConfig) -> LLMConfig:
        """Add a new LLM model"""

    def add_embedding_model(self, request: EmbeddingConfig) -> EmbeddingConfig:
        """Add a new embedding model"""

    def get_agent_context_window(self, agent_id: str, actor: User) -> ContextWindowOverview:
        luann_agent =self.load_agent(agent_id=agent_id, actor=actor)
        return  luann_agent.get_context_window()

    def run_tool_from_source(
        self,
        actor: User,
        tool_args: Dict[str, str],
        tool_source: str,
        tool_env_vars: Optional[Dict[str, str]] = None,
        tool_source_type: Optional[str] = None,
        tool_name: Optional[str] = None,
    ) -> ToolReturnMessage:
        """Run a tool from luann.source code"""
        if tool_source_type is not None and tool_source_type != "python":
            raise ValueError("Only Python source code is supported at this time")

        # NOTE: we're creating a floating Tool object and NOT persisting to DB
        tool = Tool(
            name=tool_name,
            source_code=tool_source,
        )
        assert tool.name is not None, "Failed to create tool object"

        # TODO eventually allow using agent state in tools
        agent_state = None

        # Next, attempt to run the tool with the sandbox
        try:
            sandbox_run_result = ToolExecutionSandbox(tool.name, tool_args, actor, tool_object=tool).run(
                agent_state=agent_state, additional_env_vars=tool_env_vars
            )
            return ToolReturnMessage(
                id="null",
                tool_call_id="null",
                date=get_utc_time(),
                status=sandbox_run_result.status,
                tool_return=str(sandbox_run_result.func_return),
                stdout=sandbox_run_result.stdout,
                stderr=sandbox_run_result.stderr,
            )

        except Exception as e:
            func_return = get_friendly_error_msg(function_name=tool.name, exception_name=type(e).__name__, exception_message=str(e))
            return ToolReturnMessage(
                id="null",
                tool_call_id="null",
                date=get_utc_time(),
                status="error",
                tool_return=func_return,
                stdout=[],
                stderr=[traceback.format_exc()],
            )

    

    async def send_message_to_agent(
        self,
        agent_id: str,
        actor: User,
        # role: MessageRole,
        messages: Union[List[Message], List[MessageCreate]],
        stream_steps: bool,
        stream_tokens: bool,
        # related to whether or not we return `luannMessage`s or `Message`s
        chat_completion_mode: bool = False,
        timestamp: Optional[datetime] = None,
        # Support for AssistantMessage
        use_assistant_message: bool = True,
        assistant_message_tool_name: str = constants.DEFAULT_MESSAGE_TOOL,
        assistant_message_tool_kwarg: str = constants.DEFAULT_MESSAGE_TOOL_KWARG,
        metadata: Optional[dict] = None,
    ) -> Union[StreamingResponse, LuannResponse]:
        """Split off into a separate function so that it can be imported in the /chat/completion proxy."""

        # TODO: @charles is this the correct way to handle?
        include_final_message = True

        if not stream_steps and stream_tokens:
            raise HTTPException(status_code=400, detail="stream_steps must be 'true' if stream_tokens is 'true'")

        # For streaming response
        try:

            # TODO: move this logic into server.py

            # Get the generator object off of the agent's streaming interface
            # This will be attached to the POST SSE request used under-the-hood
            luann_agent = self.load_agent(agent_id=agent_id, actor=actor)

            # Disable token streaming if not OpenAI
            # TODO: cleanup this logic
            llm_config = luann_agent.agent_state.llm_config
            if stream_tokens and (llm_config.model_endpoint_type != "openai" or "inference.memgpt.ai" in llm_config.model_endpoint):
                warnings.warn(
                    "Token streaming is only supported for models with type 'openai' or `inference.memgpt.ai` in the model_endpoint: agent has endpoint type {llm_config.model_endpoint_type} and {llm_config.model_endpoint}. Setting stream_tokens to False."
                )
                stream_tokens = False

            # Create a new interface per request
            luann_agent.interface = StreamingServerInterface(use_assistant_message)
            streaming_interface = luann_agent.interface
            if not isinstance(streaming_interface, StreamingServerInterface):
                raise ValueError(f"Agent has wrong type of interface: {type(streaming_interface)}")

            # Enable token-streaming within the request if desired
            streaming_interface.streaming_mode = stream_tokens
            # "chatcompletion mode" does some remapping and ignores inner thoughts
            streaming_interface.streaming_chat_completion_mode = chat_completion_mode

            # streaming_interface.allow_assistant_message = stream
            # streaming_interface.function_call_legacy_mode = stream

            # # Allow AssistantMessage is desired by client
            # streaming_interface.assistant_message_tool_name = assistant_message_tool_name
            # streaming_interface.assistant_message_tool_kwarg = assistant_message_tool_kwarg

            # # Related to JSON buffer reader
            # streaming_interface.inner_thoughts_in_kwargs = (
            #     llm_config.put_inner_thoughts_in_kwargs if llm_config.put_inner_thoughts_in_kwargs is not None else False
            # )

            # Offload the synchronous message_func to a separate thread
            streaming_interface.stream_start()
            task = asyncio.create_task(
                asyncio.to_thread(
                    self.send_messages,
                    actor=actor,
                    agent_id=agent_id,
                    messages=messages,
                    interface=streaming_interface,
                    metadata=metadata,
                )
            )

            if stream_steps:
                # return a stream
                return StreamingResponse(
                    sse_async_generator(
                        streaming_interface.get_generator(),
                        usage_task=task,
                        finish_message=include_final_message,
                    ),
                    media_type="text/event-stream",
                )

            else:
                # buffer the stream, then return the list
                generated_stream = []
                async for message in streaming_interface.get_generator():
                    assert (
                        isinstance(message, LuannMessage)
                        or isinstance(message, LegacyLuannMessage)
                        or isinstance(message, MessageStreamStatus)
                    ), type(message)
                    generated_stream.append(message)
                    if message == MessageStreamStatus.done:
                        break

                # Get rid of the stream status messages
                filtered_stream = [d for d in generated_stream if not isinstance(d, MessageStreamStatus)]
                usage = await task

                # By default the stream will be messages of type luannMessage or luannLegacyMessage
                # If we want to convert these to Message, we can use the attached IDs
                # NOTE: we will need to de-duplicate the Messsage IDs though (since Assistant->Inner+Func_Call)
                # TODO: eventually update the interface to use `Message` and `MessageChunk` (new) inside the deque instead
                return LuannResponse(messages=filtered_stream, usage=usage)

        except HTTPException:
            raise
        except Exception as e:
            print(e)
            import traceback

            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"{e}")
