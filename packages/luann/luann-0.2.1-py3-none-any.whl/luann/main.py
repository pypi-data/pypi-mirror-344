
import typer
from luann.cli.cli import (
    server,
    version,
)




app = typer.Typer(pretty_exceptions_enable=False)
app.command(name="version")(version)
app.command(name="server")(server)



