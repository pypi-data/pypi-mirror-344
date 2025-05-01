from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from luann.orm.mixins import OrganizationMixin
from luann.orm.sqlalchemy_base import SqlalchemyBase
from luann.schemas.providers import Provider as PydanticProvider
from sqlalchemy import Boolean, DateTime, String, func, text
if TYPE_CHECKING:
    from luann.orm.organization import Organization


class Provider(SqlalchemyBase, OrganizationMixin):
    """Provider ORM class"""

    __tablename__ = "providers"
    __pydantic_model__ = PydanticProvider

    name: Mapped[str] = mapped_column(nullable=False, doc="The name of the provider")
    api_key: Mapped[str] = mapped_column(nullable=False, doc="API key used for requests to the provider.")
    base_url: Mapped[str] = mapped_column(nullable=False, doc="base url used for requests to the provider.")

    # Azure openai
    api_version: Mapped[str] = mapped_column(nullable=False, doc="api version used for requests to the Azure provider.")

    
    # aws 
    aws_region: Mapped[str] = mapped_column(nullable=False, doc="aws region used for requests to the aws provider.")

    # vLLM  Ollama
    default_prompt_formatter: Mapped[str] = mapped_column(nullable=False, doc="Default prompt formatter (aka model wrapper) to use on vLLM /completions API.")


    #whether to enable
    # is_enabled:Mapped[str] = mapped_column(nullable=False, doc="whether  to enable the provider")
    is_enabled: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"), doc="whether  to enable the provider")

    # relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="providers")
