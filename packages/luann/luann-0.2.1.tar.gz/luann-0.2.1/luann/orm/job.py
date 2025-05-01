from datetime import datetime
from typing import TYPE_CHECKING, Optional,List

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from luann.orm.enums import JobType
from luann.orm.mixins import UserMixin
from luann.orm.sqlalchemy_base import SqlalchemyBase
from luann.schemas.enums import JobStatus
from luann.schemas.job import Job as PydanticJob
from luann.schemas.job import LuannRequestConfig
if TYPE_CHECKING:
    # from luann.orm.job_messages import JobMessage
    from luann.orm.message import Message
    from luann.orm.user import User
    # from luann.orm.step import Step


class Job(SqlalchemyBase, UserMixin):
    """Jobs run in the background and are owned by a user.
    Typical jobs involve loading and processing sources etc.
    """

    __tablename__ = "jobs"
    __pydantic_model__ = PydanticJob

    status: Mapped[JobStatus] = mapped_column(String, default=JobStatus.created, doc="The current status of the job.")
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, doc="The unix timestamp of when the job was completed.")
    metadata_: Mapped[Optional[dict]] = mapped_column(JSON, doc="The metadata of the job.")
    job_type: Mapped[JobType] = mapped_column(
        String,
        default=JobType.JOB,
        doc="The type of job. This affects whether or not we generate json_schema and source_code on the fly.",
    )
    request_config: Mapped[Optional[LuannRequestConfig]] = mapped_column(
        JSON, nullable=True, doc="The request configuration for the job, stored as JSON."
    )

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="jobs")
    # job_messages: Mapped[List["JobMessage"]] = relationship("JobMessage", back_populates="job", cascade="all, delete-orphan")
    # usage_statistics: Mapped[list["JobUsageStatistics"]] = relationship(
    #     "JobUsageStatistics", back_populates="job", cascade="all, delete-orphan"
    # )
    # steps: Mapped[List["Step"]] = relationship("Step", back_populates="job", cascade="save-update")

    # @property
    # def messages(self) -> List["Message"]:
    #     """Get all messages associated with this job."""
    #     return [jm.message for jm in self.job_messages]
