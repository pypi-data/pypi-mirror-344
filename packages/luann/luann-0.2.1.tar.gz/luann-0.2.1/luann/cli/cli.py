
import sys
from enum import Enum
from typing import Annotated, Optional
import typer
from luann.log import get_logger

logger = get_logger(__name__)
class ServerChoice(Enum):
    rest_api = "rest"
    ws_api = "websocket"

def server(
    type: Annotated[ServerChoice, typer.Option(help="Server to run")] = "rest",
    port: Annotated[Optional[int], typer.Option(help="Port to run the server on")] = None,
    host: Annotated[Optional[str], typer.Option(help="Host to run the server on (default to localhost)")] = None,
    debug: Annotated[bool, typer.Option(help="Turn debugging output on")] = False,
    secure: Annotated[bool, typer.Option(help="Adds simple security access")] = False,
):
    """Launch a luann server process"""

    if type == ServerChoice.rest_api:
        try:
            # from luann.server.rest_api.server import start_server
            from luann.server.rest_api.app import start_server
            start_server(
                port=port,
                host=host,
                debug=debug,
            )

        except KeyboardInterrupt:
            # Handle CTRL-C
            typer.secho("Terminating the server...")
            sys.exit(0)

    elif type == ServerChoice.ws_api:
        raise NotImplementedError("WS suppport deprecated")
        






def version():
  
    from luann.__init__ import __version__
    typer.secho(f"luann Current Version: {__version__}", fg=typer.colors.GREEN)
    print(__version__)
    return __version__
   
