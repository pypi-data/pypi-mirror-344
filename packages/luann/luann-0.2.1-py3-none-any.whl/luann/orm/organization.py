from typing import TYPE_CHECKING, List, Union

from sqlalchemy.orm import Mapped, mapped_column, relationship

from luann.orm.file import FileMetadata
from luann.orm.source import Source
from luann.orm.agents_tags import AgentsTags
from luann.orm.sqlalchemy_base import SqlalchemyBase
from luann.schemas.organization import Organization as PydanticOrganization

if TYPE_CHECKING:

    from luann.orm.tool import Tool
    from luann.orm.user import User
    from luann.orm.agent  import Agent
    from luann.orm.provider import Provider
 


class Organization(SqlalchemyBase):
    """The highest level of the object tree. All Entities belong to one and only one Organization."""

    __tablename__ = "organizations"
    __pydantic_model__ = PydanticOrganization

    name: Mapped[str] = mapped_column(doc="The display name of the organization.")

    # relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    tools: Mapped[List["Tool"]] = relationship("Tool", back_populates="organization", cascade="all, delete-orphan")
    blocks: Mapped[List["Block"]] = relationship("Block", back_populates="organization", cascade="all, delete-orphan")
    sources: Mapped[List["Source"]] = relationship("Source", back_populates="organization", cascade="all, delete-orphan")
    # agents_tags: Mapped[List["AgentsTags"]] = relationship("AgentsTags", back_populates="organization", cascade="all, delete-orphan")
    files: Mapped[List["FileMetadata"]] = relationship("FileMetadata", back_populates="organization", cascade="all, delete-orphan")
    sandbox_configs: Mapped[List["SandboxConfig"]] = relationship(
        "SandboxConfig", back_populates="organization", cascade="all, delete-orphan"
    )
    sandbox_environment_variables: Mapped[List["SandboxEnvironmentVariable"]] = relationship(
        "SandboxEnvironmentVariable", back_populates="organization", cascade="all, delete-orphan"
    )
    # agent_environment_variables: Mapped[List["AgentEnvironmentVariable"]] = relationship(
    #     "AgentEnvironmentVariable", back_populates="organization", cascade="all, delete-orphan"
    # )
    # TODO: Map these relationships later when we actually make these models
    # below is just a suggestion
    # agents: Mapped[List["Agent"]] = relationship("Agent", back_populates="organization", cascade="all, delete-orphan")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="organization", cascade="all, delete-orphan")
    agents: Mapped[List["Agent"]] = relationship("Agent", back_populates="organization", cascade="all, delete-orphan")
    passages: Mapped[List["Passage"]] = relationship("Passage", back_populates="organization", cascade="all, delete-orphan")
    # tools: Mapped[List["Tool"]] = relationship("Tool", back_populates="organization", cascade="all, delete-orphan")
    # documents: Mapped[List["Document"]] = relationship("Document", back_populates="organization", cascade="all, delete-orphan")
    source_passages: Mapped[List["SourcePassage"]] = relationship(
        "SourcePassage", 
        back_populates="organization", 
        cascade="all, delete-orphan"
    )
    # agent_passages: Mapped[List["AgentPassage"]] = relationship(
    #     "AgentPassage", 
    #     back_populates="organization", 
    #     cascade="all, delete-orphan"
    # )

    agent_passages: Mapped[List["AgentPassage"]] = relationship("AgentPassage", back_populates="organization", cascade="all, delete-orphan")

    providers: Mapped[List["Provider"]] = relationship("Provider", back_populates="organization", cascade="all, delete-orphan")
  
    @property
    def passages(self) -> List[Union["SourcePassage", "AgentPassage"]]:
        """Convenience property to get all passages"""
        return self.source_passages + self.agent_passages