import time
import typer
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess

app = typer.Typer()

@app.command()
def run_command(
    command: Annotated[str, typer.Option("--cmd", "-c", help="The command to run.")], 
    use_shell: Annotated[bool, typer.Option("--shell", "-s", help="Use shell mode.")]=False,
    ):
    """
    Run a command in the terminal.
    
    Args:
        command (str): The command to run.
        use_shell (bool): Whether to use shell mode.
    
    Examples:
        # List format (recommended when shell is not needed)
        run_command ls -l /tmp
        
        # String format (when shell is needed)  
        run_command "ls -l /tmp | grep log" --shell
    """
    try:
        if use_shell:
            run_command = command
        else:
            run_command = command.split()
            
        print(f"Running command: {command}")
        subprocess.run(
            run_command,
            check=True,
            shell=use_shell,
            # stderr=subprocess.PIPE,
            # stdout=subprocess.PIPE,
            # universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        exit(1)