from typing import List, Optional


from fastapi import APIRouter, Body, Depends, Header, HTTPException

from luann.errors import LuannToolCreateError
from luann.orm.errors import UniqueConstraintViolationError
from luann.schemas.luann_message import ToolReturnMessage
from luann.schemas.tool import Tool, ToolCreate, ToolRunFromSource, ToolUpdate
from luann.schemas.user import User
from luann.server.rest_api.utils import get_luann_server
from luann.server.server import SyncServer

router = APIRouter(prefix="/tools", tags=["tools"])


@router.delete("/{tool_id}", operation_id="delete_tool")
def delete_tool(
    tool_id: str,
    server: SyncServer = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Delete a tool by name
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)
    server.tool_manager.delete_tool_by_id(tool_id=tool_id, actor=actor)


@router.get("/{tool_id}", response_model=Tool, operation_id="retrieve_tool")
def retrieve_tool(
    tool_id: str,
    server: SyncServer = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Get a tool by ID
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)
    tool = server.tool_manager.get_tool_by_id(tool_id=tool_id, actor=actor)
    if tool is None:
        # return 404 error
        raise HTTPException(status_code=404, detail=f"Tool with id {tool_id} not found.")
    return tool


@router.get("/", response_model=List[Tool], operation_id="list_tools")
def list_tools(
    after: Optional[str] = None,
    limit: Optional[int] = 50,
    server: SyncServer = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Get a list of all tools available to agents belonging to the org of the user
    """
    try:
        actor = server.user_manager.get_user_or_default(user_id=user_id)
        return server.tool_manager.list_tools(actor=actor, after=after, limit=limit)
    except Exception as e:
        # Log or print the full exception here for debugging
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Tool, operation_id="create_tool")
def create_tool(
    request: ToolCreate = Body(...),
    server: SyncServer = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Create a new tool
    """
    try:
        actor = server.user_manager.get_user_or_default(user_id=user_id)
        tool = Tool(**request.model_dump())
        return server.tool_manager.create_tool(pydantic_tool=tool, actor=actor)
    except UniqueConstraintViolationError as e:
        # Log or print the full exception here for debugging
        print(f"Error occurred: {e}")
        clean_error_message = f"Tool with this name already exists."
        raise HTTPException(status_code=409, detail=clean_error_message)
    except LuannToolCreateError as e:
        # HTTP 400 == Bad Request
        print(f"Error occurred during tool creation: {e}")
        # print the full stack trace
        import traceback

        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch other unexpected errors and raise an internal server error
        print(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.put("/", response_model=Tool, operation_id="upsert_tool")
def upsert_tool(
    request: ToolCreate = Body(...),
    server: SyncServer = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),
):
    """
    Create or update a tool
    """
    try:
        actor = server.user_manager.get_user_or_default(user_id=user_id)
        tool = server.tool_manager.create_or_update_tool(pydantic_tool=Tool(**request.model_dump()), actor=actor)
        return tool
    except UniqueConstraintViolationError as e:
        # Log the error and raise a conflict exception
        print(f"Unique constraint violation occurred: {e}")
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        # Catch other unexpected errors and raise an internal server error
        print(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.patch("/{tool_id}", response_model=Tool, operation_id="modify_tool")
def modify_tool(
    tool_id: str,
    request: ToolUpdate = Body(...),
    server: SyncServer = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Update an existing tool
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)
    return server.tool_manager.update_tool_by_id(tool_id=tool_id, tool_update=request, actor=actor)


@router.post("/add-base-tools", response_model=List[Tool], operation_id="add_base_tools")
def upsert_base_tools(
    server: SyncServer = Depends(get_luann_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Upsert base tools
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)
    return server.tool_manager.upsert_base_tools(actor=actor)


@router.post("/run", response_model=ToolReturnMessage, operation_id="run_tool_from_source")
def run_tool_from_source(
    server: SyncServer = Depends(get_luann_server),
    request: ToolRunFromSource = Body(...),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from luann.header, default to None if not present
):
    """
    Attempt to build a tool from luann.source, then run it on the provided arguments
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    try:
        return server.run_tool_from_source(
            tool_source=request.source_code,
            tool_source_type=request.source_type,
            tool_args=request.args,
            tool_env_vars=request.env_vars,
            tool_name=request.name,
            actor=actor,
        )
    except LuannToolCreateError as e:
        # HTTP 400 == Bad Request
        print(f"Error occurred during tool creation: {e}")
        # print the full stack trace
        import traceback

        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Catch other unexpected errors and raise an internal server error
        print(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


