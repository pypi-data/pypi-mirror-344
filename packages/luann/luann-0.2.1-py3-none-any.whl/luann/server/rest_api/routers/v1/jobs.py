from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from luann.orm.errors import NoResultFound
from luann.schemas.enums import JobStatus
from luann.schemas.job import Job
from luann.server.rest_api.utils import get_luann_server
from luann.server.server import SyncServer

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[Job], operation_id="list_jobs")
def list_jobs(
    server: "SyncServer" = Depends(get_luann_server),
    source_id: Optional[str] = Query(None, description="Only list jobs associated with the source."),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    List all jobs.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    # TODO: add filtering by status
    jobs = server.job_manager.list_jobs(actor=actor)

    # TODO: eventually use ORM
    # results = session.query(JobModel).filter(JobModel.user_id == user_id, JobModel.metadata_["source_id"].astext == sourced_id).all()
    if source_id:
        # can't be in the ORM since we have source_id stored in the metadata_
        jobs = [job for job in jobs if job.metadata_.get("source_id") == source_id]
    return jobs


@router.get("/active", response_model=List[Job], operation_id="list_active_jobs")
def list_active_jobs(
    server: "SyncServer" = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    List all active jobs.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    return server.job_manager.list_jobs(actor=actor, statuses=[JobStatus.created, JobStatus.running])


@router.get("/{job_id}", response_model=Job, operation_id="retrieve_job")
def retrieve_job(
    job_id: str,
    user_id: Optional[str] = Header(None, alias="user_id"),
    server: "SyncServer" = Depends(get_luann_server),
):
    """
    Get the status of a job.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    try:
        return server.job_manager.get_job_by_id(job_id=job_id, actor=actor)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Job not found")



@router.delete("/{job_id}", response_model=Job, operation_id="delete_job")
def delete_job(
    job_id: str,
    user_id: Optional[str] = Header(None, alias="user_id"),
    server: "SyncServer" = Depends(get_luann_server),
):
    """
    Delete a job by its job_id.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    try:
        job = server.job_manager.delete_job_by_id(job_id=job_id, actor=actor)
        return job
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Job not found")
