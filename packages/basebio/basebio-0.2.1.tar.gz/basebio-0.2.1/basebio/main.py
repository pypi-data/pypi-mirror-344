import typer
from .modules.cmdtools import run_command

app = typer.Typer(add_completion=False)

@app.callback()
def callback():
    """
    BaseBio is a Python package for bioinformatics.
    """

app.command(name="cmd")(run_command)


if __name__ == "__main__":
    app()