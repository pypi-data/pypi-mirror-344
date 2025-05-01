from typing import TYPE_CHECKING,List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from luann.orm.mixins import OrganizationMixin
from luann.orm.sqlalchemy_base import SqlalchemyBase
from luann.schemas.user import User as PydanticUser
# from luann.orm.user_token  import UserToken

if TYPE_CHECKING:
    from luann.orm.organization import Organization
    from luann.orm import Job, Organization
    # from luann.orm.user_token  import UserToken



class User(SqlalchemyBase, OrganizationMixin):
    """User ORM class"""

    __tablename__ = "users"
    __pydantic_model__ = PydanticUser

    name: Mapped[str] = mapped_column(nullable=False, doc="The display name of the user.")

    # relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="users")
    jobs: Mapped[List["Job"]] = relationship(
        "Job", back_populates="user", doc="the jobs associated with this user.", cascade="all, delete-orphan"
    )
    # TODO: Add this back later potentially
    # agents: Mapped[List["Agent"]] = relationship(
    #     "Agent", secondary="users_agents", back_populates="users", doc="the agents associated with this user."
    # )
    # user_tokens: Mapped[List["UserToken"]] = relationship("UserToken", back_populates="users", doc="the tokens associated with this user.")
    # jobs: Mapped[List["Job"]] = relationship("Job", back_populates="user", doc="the jobs associated with this user.")
