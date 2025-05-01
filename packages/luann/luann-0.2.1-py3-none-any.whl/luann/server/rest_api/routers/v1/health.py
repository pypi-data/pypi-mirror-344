from typing import TYPE_CHECKING

from fastapi import APIRouter

from luann.cli.cli import version
from luann.schemas.healty import Health

if TYPE_CHECKING:
    pass

router = APIRouter(prefix="/health", tags=["health"])


# Health check
@router.get("/", response_model=Health, operation_id="health_check")
def health_check():
    return Health(
        version=version(),
        status="ok",
    )
