from typing import TYPE_CHECKING, List,Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint,JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index
from luann.orm.mixins import UserMixin,AgentMixin,OrganizationMixin
from luann.orm.sqlalchemy_base import SqlalchemyBase
from luann.orm.custom_columns import ToolCallColumn
# from luann.orm.agents_tags import AgentsTags
from luann.schemas.message import Message as PydanticMessage
from luann.schemas.message import TextContent as PydanticTextContent

from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall as OpenAIToolCall

if TYPE_CHECKING:
    from luann.orm.organization import Organization
    # from luann.orm.step import Step



class Message(SqlalchemyBase,AgentMixin,OrganizationMixin):
    """Associates tags with agents, allowing agents to have multiple tags and supporting tag-based filtering."""

    __tablename__ = "messages"
    __pydantic_model__ = PydanticMessage
    __table_args__ = (Index("ix_messages_agent_created_at", "agent_id", "created_at"),)
    # __table_args__ = (UniqueConstraint("id", "name", name="unique_agent name"),)
    
    id: Mapped[str] = mapped_column(primary_key=True, doc="Unique message identifier")
    role: Mapped[str] = mapped_column(doc="Message role (user/assistant/system/tool)")
    text: Mapped[Optional[str]] = mapped_column(nullable=True, doc="Message content")
    model: Mapped[Optional[str]] = mapped_column(nullable=True, doc="LLM model used")
    name: Mapped[Optional[str]] = mapped_column(nullable=True, doc="Name for multi-agent scenarios")
    tool_calls: Mapped[OpenAIToolCall] = mapped_column(ToolCallColumn, doc="Tool call information")
    tool_call_id: Mapped[Optional[str]] = mapped_column(nullable=True, doc="ID of the tool call")
    # step_id: Mapped[Optional[str]] = mapped_column(
    #     ForeignKey("steps.id", ondelete="SET NULL"), nullable=True, doc="ID of the step that this message belongs to"
    # )

    #relationship
    # tool_calls: Mapped[Optional[List[ToolCall]]] = relationship("ToolCall",back_populates="message", cascade="all, delete-orphan")
     #relationship
    agent: Mapped["Agent"] = relationship("Agent", back_populates="messages", lazy="selectin")
    organization: Mapped["Organization"] = relationship("Organization", back_populates="messages", lazy="selectin")
    # step: Mapped["Step"] = relationship("Step", back_populates="messages", lazy="selectin")

    # # Job relationship
    # job_message: Mapped[Optional["JobMessage"]] = relationship(
    #     "JobMessage", back_populates="message", uselist=False, cascade="all, delete-orphan", single_parent=True
    # )

    # @property
    # def job(self) -> Optional["Job"]:
    #     """Get the job associated with this message, if any."""
    #     return self.job_message.job if self.job_message else None
    def to_pydantic(self) -> PydanticMessage:
        # print(f"model message")
        """custom pydantic conversion for message content mapping"""
        model = self.__pydantic_model__.model_validate(self)
        # print(f"model message :{model.tool_calls}")
        if self.text:
            model.content = [PydanticTextContent(text=self.text)]
        return model

    

   
