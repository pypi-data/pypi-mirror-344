import subprocess
import platform
from typing import Dict

def run_shell(
    command: str,
    *,
    check: bool = True,
    capture_output: bool = False,
    text: bool = True,
    interactive: bool = False,
    shell_preference: str = "auto",
    **kwargs: Dict
) -> subprocess.CompletedProcess:
    """
    Run a command in a bash shell (optionally as an interactive shell).

    Args:
        command: The shell command to execute (as a string).
        check: If True, raises CalledProcessError on non-zero exit.
        capture_output: If True, captures and returns stdout/stderr.
        text: If True, treats input/output as strings; if False, uses bytes.
        interactive: If True, runs bash in interactive mode (-i).
        **kwargs: Additional arguments passed to subprocess.run.

    Returns:
        subprocess.CompletedProcess: The result of the executed process.
    """
    shell_args = resolve_shell_command(
        command,
        interactive=interactive,
        shell_preference=shell_preference
    )

    return subprocess.run(
        shell_args,
        check=check,
        capture_output=capture_output,
        text=text,
        **kwargs
    )


def resolve_shell_command(command: str, *, interactive: bool, shell_preference: str = "auto") -> list[str]:
    system = platform.system().lower()

    # ---- macOS / Linux ----
    if system in ("linux", "darwin"):
        shell = "bash"

        if shell_preference == "zsh":
            shell = "zsh"
        elif shell_preference == "bash":
            shell = "bash"

        shell_args = [shell]
        if interactive:
            shell_args.append("-i")
        shell_args += ["-c", command]
        return shell_args

    # ---- Windows ----
    elif system == "windows":
        if shell_preference == "powershell":
            return ["powershell", "-Command", command]
        else:
            return ["cmd", "/C", command]

    # ---- Unsupported ----
    raise RuntimeError(f"Unsupported platform: {system}")