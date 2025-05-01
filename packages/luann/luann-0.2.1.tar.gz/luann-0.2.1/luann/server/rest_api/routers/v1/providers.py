from typing import TYPE_CHECKING, List, Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query

from luann.schemas.providers import Provider, ProviderCreate, ProviderUpdate
from luann.server.rest_api.utils import get_luann_server

if TYPE_CHECKING:
    from luann.server.server import SyncServer

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("/", tags=["providers"], response_model=List[Provider], operation_id="list_providers")
def list_providers(
    after: Optional[str] = Query(None),
    limit: Optional[int] = Query(50),
    server: "SyncServer" = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Get a list of all custom providers in the database
    """
    try:
        actor = server.user_manager.get_user_or_default(user_id=user_id)
        providers = server.provider_manager.list_providers(actor=actor,after=after, limit=limit)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    return providers


@router.get("/privider_name/", tags=["providers"], response_model=List[str], operation_id="list_enabled_providers_name")
def list_enabled_providers_name(
    server: "SyncServer" = Depends(get_luann_server),
):
    """
    Get a list of all custom providers in the database
    """
    try:
        providers_name = server.provider_manager.list_enabled_providers_name()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    return providers_name


@router.post("/", tags=["providers"], response_model=Provider, operation_id="create_provider")
def create_provider(
    request: ProviderCreate = Body(...),
    server: "SyncServer" = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Create a new custom provider
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    provider = Provider(**request.model_dump())
    provider = server.provider_manager.create_provider(provider, actor=actor)
    return provider


@router.patch("/", tags=["providers"], response_model=Provider, operation_id="modify_provider")
def modify_provider(
    request: ProviderUpdate = Body(...),
    server: "SyncServer" = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Update an existing custom provider
    """

    actor = server.user_manager.get_user_or_default(user_id=user_id)
    provider = server.provider_manager.update_provider(request, actor=actor)
    return provider


@router.delete("/", tags=["providers"], response_model=None, operation_id="delete_provider")
def delete_provider(
    provider_id: str = Query(..., description="The provider_id key to be deleted."),
    server: "SyncServer" = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Delete an existing custom provider
    """
    try:
        actor = server.user_manager.get_user_or_default(user_id=user_id)
        server.provider_manager.delete_provider_by_id(provider_id=provider_id, actor=actor)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
