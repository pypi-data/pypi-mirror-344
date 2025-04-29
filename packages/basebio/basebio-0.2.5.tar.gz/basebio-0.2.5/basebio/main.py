import typer
from .modules.cmd import run

app = typer.Typer(add_completion=False)

@app.callback()
def callback():
    """
    BaseBio is a Python package for bioinformatics.
    """

app.command(name="cmd")(run)


if __name__ == "__main__":
    app()