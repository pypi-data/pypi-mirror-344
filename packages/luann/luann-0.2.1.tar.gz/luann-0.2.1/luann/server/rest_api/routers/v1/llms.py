from typing import TYPE_CHECKING, List,Optional

from fastapi import APIRouter, Depends,Header

from luann.schemas.embedding_config import EmbeddingConfig
from luann.schemas.llm_config import LLMConfig
from luann.server.rest_api.utils import get_luann_server
from luann.schemas.user import User

if TYPE_CHECKING:
    from luann.server.server import SyncServer

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=List[LLMConfig], operation_id="list_models")
def list_llm_backends(
    server: "SyncServer" = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    


    actor = server.user_manager.get_user_or_default(user_id=user_id)
    models = server.list_llm_models(actor=actor)
    # print(models)
    return models


@router.get("/embedding", response_model=List[EmbeddingConfig], operation_id="list_embedding_models")
def list_embedding_backends(
    server: "SyncServer" = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    
    actor = server.user_manager.get_user_or_default(user_id=user_id)
    models = server.list_embedding_models(actor=actor)
    # print(models)
    return models
