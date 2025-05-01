from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

# TODO everything in functions should live in this model
from luann.orm.enums import ToolSourceType,ToolType
from luann.orm.mixins import OrganizationMixin,AgentMixin
from luann.orm.sqlalchemy_base import SqlalchemyBase
from luann.schemas.tool import Tool as PydanticTool
# from luann.orm.tools_agents import ToolAgents
if TYPE_CHECKING:
    from luann.orm.organization import Organization


class Tool(SqlalchemyBase, OrganizationMixin):
    """Represents an available tool that the LLM can invoke.

    NOTE: polymorphic inheritance makes more sense here as a TODO. We want a superset of tools
    that are always available, and a subset scoped to the organization. Alternatively, we could use the apply_access_predicate to build
    more granular permissions.
    """

    __tablename__ = "tools"
    __pydantic_model__ = PydanticTool

    # Add unique constraint on (name, _organization_id)
    # An organization should not have multiple tools with the same name
    __table_args__ = (UniqueConstraint("name", "organization_id", name="uix_name_organization"),)

    name: Mapped[str] = mapped_column(doc="The display name of the tool.")
    tool_type: Mapped[ToolType] = mapped_column(
        String,
        default=ToolType.CUSTOM,
        doc="The type of tool. This affects whether or not we generate json_schema and source_code on the fly.",
    )
    # return_char_limit: Mapped[int] = mapped_column(nullable=True, doc="The maximum number of characters the tool can return.")
    
    description: Mapped[Optional[str]] = mapped_column(nullable=True, doc="The description of the tool.")
    tags: Mapped[List] = mapped_column(JSON, doc="Metadata tags used to filter tools.")
    return_char_limit: Mapped[int] = mapped_column(nullable=True, doc="The maximum number of characters the tool can return.")
    source_type: Mapped[ToolSourceType] = mapped_column(String, doc="The type of the source code.", default=ToolSourceType.json)
    source_code: Mapped[Optional[str]] = mapped_column(String, doc="The source code of the function.")
    json_schema: Mapped[dict] = mapped_column(JSON, default=lambda: {}, doc="The OAI compatable JSON schema of the function.")
    # module: Mapped[Optional[str]] = mapped_column(
    #     String, nullable=True, doc="the module path from luann.which this tool was derived in the codebase."
    # )

    # relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="tools", lazy="selectin")
    # tool_agents: Mapped["ToolAgents"] = relationship("ToolAgents", back_populates="tools")
