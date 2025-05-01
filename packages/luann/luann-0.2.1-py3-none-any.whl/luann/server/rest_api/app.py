import json
import logging
import sys
from pathlib import Path
from typing import Optional
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from luann.__init__ import __version__
from luann.constants import ADMIN_PREFIX, API_PREFIX
from luann.schemas.luann_response import LuannResponse
from luann.server.constants import REST_DEFAULT_PORT


from luann.server.rest_api.auth.index import (
    setup_auth_router,  # TODO: probably remove right?
)
from luann.server.rest_api.interface import StreamingServerInterface
from luann.server.rest_api.routers.v1 import ROUTERS as v1_routes
from luann.server.rest_api.routers.v1.organizations import (
    router as organizations_router,
)
from luann.server.rest_api.routers.v1.users import (
    router as users_router,  # TODO: decide on admin
)
# from luann.server.rest_api.static_files import mount_static_files
from luann.server.server import SyncServer
from luann.settings import settings


interface: StreamingServerInterface = StreamingServerInterface
server = SyncServer(default_interface_factory=lambda: interface())
password = None
import logging
# from fastapi import FastAPI
log = logging.getLogger("uvicorn")





# middleware that only allows requests to pass through if user provides a password thats randomly generated and stored in memory
def generate_password():
    import secrets

    return secrets.token_urlsafe(16)


random_password =os.getenv("luann_SERVER_PASSWORD") or generate_password()


class CheckPasswordMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
         # Exclude health check endpoint from luann.password protection
        if request.url.path == "/v1/health/" or request.url.path == "/latest/health/":
            return await call_next(request)
        if request.headers.get("X-BARE-PASSWORD") == f"password {random_password}":
            return await call_next(request)

        return JSONResponse(
            content={"detail": "Unauthorized"},
            status_code=401,
        )


def create_application() -> "FastAPI":
    """the application start routine"""
    # global server
    # server = SyncServer(default_interface_factory=lambda: interface())
    # print(f"\n[[ Luann server // v{__version__} ]]")

    app = FastAPI(
        swagger_ui_parameters={"docExpansion": "none"},
        # openapi_tags=TAGS_METADATA,
        title="Luann",
        summary="Create LLM agents with long-term memory and custom tools 📚🦙",
        version="0.2.0",  # TODO wire this up to the version in the package
        debug=True,
    )
    

    if "--secure" in sys.argv:
        print(f"▶ Using secure mode with password: {random_password}")
        app.add_middleware(CheckPasswordMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for route in v1_routes:
        app.include_router(route, prefix=API_PREFIX)
        # this gives undocumented routes for "latest" and bare api calls.
        # we should always tie this to the newest version of the api.
        # app.include_router(route, prefix="", include_in_schema=False)
        app.include_router(route, prefix="/latest", include_in_schema=False)

    # NOTE: ethan these are the extra routes
    # TODO(ethan) remove

    # admin/users
    app.include_router(users_router, prefix=ADMIN_PREFIX)
    app.include_router(organizations_router, prefix=ADMIN_PREFIX)

    # # openai
    # app.include_router(openai_assistants_router, prefix=OPENAI_API_PREFIX)
    # app.include_router(openai_threads_router, prefix=OPENAI_API_PREFIX)
    # app.include_router(openai_chat_completions_router, prefix=OPENAI_API_PREFIX)

    # /api/auth endpoints
    app.include_router(setup_auth_router(server, interface, password), prefix=API_PREFIX)

    # / static files
    # mount_static_files(app)

    @app.on_event("startup")
    def on_startup():
        pass
        # load the default tools
        # from luann.luann.orm.tool import Tool

        # Tool.load_default_tools(get_db_session())

        # generate_openapi_schema(app)

    @app.on_event("shutdown")
    def on_shutdown():
        global server
        # server.save_agents()
        # server = None

    return app


app = create_application()


def start_server(
    port: Optional[int] = None,
    host: Optional[str] = None,
    debug: bool = False,
):
    """Convenience method to start the server from luann.within Python"""
    if debug:
        from luann.server.server import logger as server_logger

        # Set the logging level
        server_logger.setLevel(logging.DEBUG)
        # Create a StreamHandler
        stream_handler = logging.StreamHandler()
        # Set the formatter (optional)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(formatter)
        # Add the handler to the logger
        server_logger.addHandler(stream_handler)

    print(f"▶ Server running at: http://{host or 'localhost'}:{port or REST_DEFAULT_PORT}\n")
    uvicorn.run(
        app,
        host=host or "localhost",
        port=port or REST_DEFAULT_PORT,
    )
    
