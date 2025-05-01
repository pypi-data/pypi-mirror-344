from typing import TYPE_CHECKING, List,Optional
import uuid
from sqlalchemy import String, UniqueConstraint,JSON,Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from luann.orm.mixins import OrganizationMixin,MessageMixin
from luann.orm.sqlalchemy_base import SqlalchemyBase

from luann.orm.block import Block
from luann.orm.custom_columns import (
    EmbeddingConfigColumn,
    LLMConfigColumn,
    # ToolRulesColumn,
)

from luann.orm.message import Message
from luann.constants import MULTI_AGENT_TOOLS
from luann.schemas.agent import AgentState as PydanticAgentState
from luann.schemas.agent import AgentType
from luann.schemas.embedding_config import EmbeddingConfig
from luann.schemas.llm_config import LLMConfig
from luann.schemas.memory import Memory
# from luann.schemas.tool_rule import ToolRule,TerminalToolRule
from luann.orm.tool  import  Tool

if TYPE_CHECKING:
    from luann.orm.organization import Organization
    from luann.orm.agents_tags import  AgentsTags
    from luann.orm.source import Source
    from luann.orm.tool  import  Tool
    # from luann.schemas.agent import AgentState as PydanticAgentState
   
    
class Agent(SqlalchemyBase, OrganizationMixin):
    """Associates tags with agents, allowing agents to have multiple tags and supporting tag-based filtering."""

    __tablename__ = "agents"
    __pydantic_model__ = PydanticAgentState
    __table_args__ = (Index("ix_agents_created_at", "created_at", "id"),)


    # agent generates its own id
    # TODO: We want to migrate all the ORM models to do this, so we will need to move this to the SqlalchemyBase
    # TODO: Some still rely on the Pydantic object to do this
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: f"agent-{uuid.uuid4()}")

    # Descriptor fields
    agent_type: Mapped[Optional[AgentType]] = mapped_column(String, nullable=True, doc="The type of Agent")
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True, doc="a human-readable identifier for an agent, non-unique.")
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True, doc="The description of the agent.")

    # System prompt
    system: Mapped[Optional[str]] = mapped_column(String, nullable=True, doc="The system prompt used by the agent.")

    # In context memory
    # TODO: This should be a separate mapping table
    # This is dangerously flexible with the JSON type
    message_ids: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, doc="List of message IDs in in-context memory.")

    # Metadata and configs
    metadata_: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, doc="metadata for the agent.")
    llm_config: Mapped[Optional[LLMConfig]] = mapped_column(
        LLMConfigColumn, nullable=True, doc="the LLM backend configuration object for this agent."
    )
    embedding_config: Mapped[Optional[EmbeddingConfig]] = mapped_column(
        EmbeddingConfigColumn, doc="the embedding configuration object for this agent."
    )

    # Tool rules
    # tool_rules: Mapped[Optional[List[ToolRule]]] = mapped_column(ToolRulesColumn, doc="the tool rules for this agent.")

    # relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="agents")
    # tool_exec_environment_variables: Mapped[List["AgentEnvironmentVariable"]] = relationship(
    #     "AgentEnvironmentVariable",
    #     back_populates="agent",
    #     cascade="all, delete-orphan",
    #     lazy="selectin",
    #     doc="Environment variables associated with this agent.",
    # )
    tools: Mapped[List["Tool"]] = relationship("Tool", secondary="tools_agents", lazy="selectin", passive_deletes=True)
    sources: Mapped[List["Source"]] = relationship("Source", secondary="sources_agents", lazy="selectin")
    # core_memory: Mapped[List["Block"]] = relationship("Block", secondary="blocks_agents", lazy="selectin")

    core_memory: Mapped[List["Block"]] = relationship(
        "Block",
        secondary="blocks_agents",
        lazy="selectin",
        passive_deletes=True,  # Ensures SQLAlchemy doesn't fetch blocks_agents rows before deleting
        back_populates="agents",
        doc="Blocks forming the core memory of the agent.",
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="agent",
        lazy="selectin",
        cascade="all, delete-orphan",  # Ensure messages are deleted when the agent is deleted
        passive_deletes=True,
    )
    tags: Mapped[List["AgentsTags"]] = relationship(
        "AgentsTags",
        back_populates="agent",
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="Tags associated with the agent.",
    )
    source_passages: Mapped[List["SourcePassage"]] = relationship(
        "SourcePassage",
        secondary="sources_agents",  # The join table for Agent -> Source
        primaryjoin="Agent.id == sources_agents.c.agent_id",
        secondaryjoin="and_(SourcePassage.source_id == sources_agents.c.source_id)",
        lazy="selectin",
        order_by="SourcePassage.created_at.desc()",
        viewonly=True,  # Ensures SQLAlchemy doesn't attempt to manage this relationship
        doc="All passages derived from luann.sources associated with this agent.",
    )
    agent_passages: Mapped[List["AgentPassage"]] = relationship(
        "AgentPassage",
        back_populates="agent",
        lazy="selectin",
        order_by="AgentPassage.created_at.desc()",
        cascade="all, delete-orphan",
        viewonly=True,  # Ensures SQLAlchemy doesn't attempt to manage this relationship
        doc="All passages derived created by this agent.",
    )

    def to_pydantic(self) -> PydanticAgentState:
        """converts to the basic pydantic model counterpart"""
        # print(f"self.core_memory:{self.core_memory}")
        # tool_rules = self.tool_rules
        # if not tool_rules:
        #     tool_rules = [
        #         TerminalToolRule(tool_name="send_message"),
        #     ]

        #     for tool_name in MULTI_AGENT_TOOLS:
        #         tool_rules.append(TerminalToolRule(tool_name=tool_name))

        state = {
            "id": self.id,
            "organization_id": self.organization_id,
            "name": self.name,
            "description": self.description,
            "message_ids": self.message_ids,
            "tools": self.tools,
            "sources": [source.to_pydantic() for source in self.sources],
            "tags": [t.tag for t in self.tags],
            # "tool_rules": self.tool_rules,
            "system": self.system,
            "agent_type": self.agent_type,
            "llm_config": self.llm_config,
            "embedding_config": self.embedding_config,
            "metadata_": self.metadata_,
            "memory": Memory(blocks=[b.to_pydantic() for b in self.core_memory]),
            "created_by_id": self.created_by_id,
            "last_updated_by_id": self.last_updated_by_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            # "tool_exec_environment_variables": self.tool_exec_environment_variables,
        }
        return self.__pydantic_model__(**state)
