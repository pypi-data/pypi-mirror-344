from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String,Index
from sqlalchemy.orm import Mapped, mapped_column, relationship,declared_attr

from luann.config import LuannConfig
from luann.constants import MAX_EMBEDDING_DIM
from luann.orm.custom_columns import CommonVector
from luann.orm.mixins import FileMixin, OrganizationMixin,SourceMixin,AgentMixin
from luann.orm.source import EmbeddingConfigColumn
from luann.orm.sqlalchemy_base import SqlalchemyBase
from luann.schemas.passage import Passage as PydanticPassage
from luann.settings import settings

config = LuannConfig()

if TYPE_CHECKING:
    from luann.orm.organization import Organization


# TODO: After migration to Passage, will need to manually delete passages where files
#       are deleted on web
class BasePassage(SqlalchemyBase, OrganizationMixin):
    """Base class for all passage types with common fields"""

    __abstract__ = True
    __pydantic_model__ = PydanticPassage

    id: Mapped[str] = mapped_column(primary_key=True, doc="Unique passage identifier")
    text: Mapped[str] = mapped_column(doc="Passage text content")
    embedding_config: Mapped[dict] = mapped_column(EmbeddingConfigColumn, doc="Embedding configuration")
    metadata_: Mapped[dict] = mapped_column(JSON, doc="Additional metadata")

    # Vector embedding field based on database type
    if settings.luann_pg_uri_no_default:
        from pgvector.sqlalchemy import Vector

        embedding = mapped_column(Vector(MAX_EMBEDDING_DIM))
    else:
        embedding = Column(CommonVector)

    @declared_attr
    def organization(cls) -> Mapped["Organization"]:
        """Relationship to organization"""
        return relationship("Organization", back_populates="passages", lazy="selectin")

    @declared_attr
    def __table_args__(cls):
        if settings.luann_pg_uri_no_default:
            return (
                Index(f"{cls.__tablename__}_org_idx", "organization_id"),
                Index(f"{cls.__tablename__}_created_at_id_idx", "created_at", "id"),
                {"extend_existing": True},
            )
        return (Index(f"{cls.__tablename__}_created_at_id_idx", "created_at", "id"), {"extend_existing": True})


class SourcePassage(BasePassage, FileMixin, SourceMixin):
    """Passages derived from luann.external files/sources"""

    __tablename__ = "source_passages"

    @declared_attr
    def file(cls) -> Mapped["FileMetadata"]:
        """Relationship to file"""
        return relationship("FileMetadata", back_populates="source_passages", lazy="selectin")

    @declared_attr
    def organization(cls) -> Mapped["Organization"]:
        return relationship("Organization", back_populates="source_passages", lazy="selectin")

    @declared_attr
    def source(cls) -> Mapped["Source"]:
        """Relationship to source"""
        return relationship("Source", back_populates="passages", lazy="selectin", passive_deletes=True)


class AgentPassage(BasePassage, AgentMixin):
    """Passages created by agents as archival memories"""

    __tablename__ = "agent_passages"

    @declared_attr
    def organization(cls) -> Mapped["Organization"]:
        return relationship("Organization", back_populates="agent_passages", lazy="selectin")

    @declared_attr
    def agent(cls) -> Mapped["Agent"]:
        """Relationship to agent"""
        return relationship("Agent", back_populates="agent_passages", lazy="selectin", passive_deletes=True)