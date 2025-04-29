#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File    : pyborg
Author  : A. Dareau

Comments:
"""

# % IMPORTS

# std library
import subprocess
import configparser
from pathlib import Path


# external dependencies
import typer
from typing_extensions import Annotated
from rich import print

# % GLOBAL

# configuration files
CONFIG_DIR = Path.home() / ".config" / "pyborg"
PROFILES_FILE = CONFIG_DIR / "profiles.cfg"
REQUIRED_FIELDS = [
    "description",
    "sudo",
    "source",
    "repository",
    "save_fmt",
    "option",
    "compression",
]
# display
HEADER = ". [green]{}[/green]\n"
PARAM = "  ├── {} : {}\n"
LPARAM = "  └── {} : {}\n"

# % DEFINE APP

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True
)


# % FUNCTIONS


def load_profile(profile: str):
    """
    Loads a given profile
    """
    # -- check if config file exists
    if not PROFILES_FILE.is_file():
        msg = f"Cannot find the profile config file at '{PROFILES_FILE}'. "
        msg += "You can initialize a config file using `pyborg init`."
        print(msg)
        raise typer.Abort()

    # -- load
    config = configparser.ConfigParser(interpolation=None)
    config.read(PROFILES_FILE)

    # -- does the profile exist ?
    if profile not in config.sections():
        print(f"[bold red]Error :[/bold red]  Cannot find profile '{profile}' !")
        print(f">> available profiles : [green]{', '.join(config.sections())}[/green]")
        raise typer.Abort()

    # -- load profile
    profile_info = config[profile]

    # -- check all fields are here
    for field in REQUIRED_FIELDS:
        if field not in profile_info:
            print(
                f"[bold red]Error :[/bold red]  missing field for profile '{profile}' !"
            )
            print(f">> required field '{field}' not found !")
            raise typer.Abort()

    return profile_info


# % DEFINE COMMANDS


@app.command()
def profiles(
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="show profiles settings")
    ] = False,
):
    "Lists available borg profiles"
    # -- check if config file exists
    if not PROFILES_FILE.is_file():
        msg = f"Cannot find the profile config file at '{PROFILES_FILE}'. "
        msg += "You can initialize a config file using `pyborg init`."
        print(msg)
        raise typer.Abort()

    # -- load config
    config = configparser.ConfigParser(interpolation=None)
    config.read(PROFILES_FILE)

    # -- print title
    msg = " 📄 List of Backup Profiles "
    n = len(msg) + 1
    print("╭" + "─" * n + "╮")
    print(f"│[bold blue]{msg}[/bold blue]│")
    print("╰" + "─" * n + "╯")

    # -- print profiles
    for s in config.sections():
        info = HEADER.format(s)
        if verbose:
            out = []
            for param, value in config[s].items():
                out.append(PARAM.format(param, value))
            out.pop()
            out.append(LPARAM.format(param, value))
            info += "".join(out)
        print(info)


@app.command()
def mount(
    profile: Annotated[str, typer.Argument(help="Profile to mount")],
    target: Annotated[
        Path,
        typer.Option(
            "--target",
            "-t",
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
            resolve_path=True,
            help="where to mount",
        ),
    ] = Path("/mnt/borg"),
    last: Annotated[
        int,
        typer.Option(
            "--last",
            "-l",
            help="consider last N archives after other filters were applied",
        ),
    ] = 0,
):
    """
    [blue]Mounts[/blue] a borg repository
    """
    # -- get profile info
    profile_info = load_profile(profile)

    # -- prepare prompt
    # arguments
    if last > 0:
        opt = f"--last {last} "
    else:
        opt = ""
    repo = profile_info["repository"]
    # prompt
    prompt = f"borg mount {opt}{repo} {target}"

    # -- print and execute
    print(f"[bold blue]Running :[/bold blue] $> {prompt}")
    subprocess.run(prompt, shell=True)


@app.command()
def save(
    profile: Annotated[str, typer.Argument(help="Profile to mount")],
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry",
            "-d",
            help="performs a dry run",
        ),
    ] = False,
):
    """
    [blue]Creates[/blue] a new backup
    """
    # -- get profile info
    profile_info = load_profile(profile)

    # -- prepare prompt
    # arguments
    repository = profile_info["repository"]
    source = profile_info["source"]
    save_fmt = profile_info["save_fmt"]
    option = profile_info["option"]
    compression = profile_info["compression"]
    if dry_run > 0:
        dry = "--dry-run"
    else:
        dry = ""
    if profile_info["sudo"].upper() == "TRUE":
        sudo = "sudo "
    else:
        sudo = ""
    print(sudo)

    # prompt
    prompt = f"{sudo} borg create {dry} --progress -v --stats --compression {compression} {option} {repository}::{save_fmt} {source}"
    # -- print and execute
    print(f"[bold blue]Running :[/bold blue] $> {prompt}")
    typer.confirm("Shall we proceed ?", abort=True)
    subprocess.run(prompt, shell=True)


@app.command()
def umount(
    target: Annotated[
        Path,
        typer.Option(
            "--target",
            "-t",
            exists=False,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="target to unmount",
        ),
    ] = Path("/mnt/borg")
):
    """
    [blue]Unmounts[/blue] a borg repository
    """

    # prompt
    prompt = f"borg umount {target}"

    # -- print and execute
    print(f"[bold blue]Running :[/bold blue] $> {prompt}")
    subprocess.run(prompt, shell=True)


@app.command()
def list(
    profile: Annotated[str, typer.Argument(help="Profile to mount")],
    last: Annotated[
        int,
        typer.Option(
            "--last",
            "-l",
            help="consider last N archives after other filters were applied",
        ),
    ] = 0,
):
    """
    [blue]Lists[/blue] the content of a borg repository
    """
    # -- get profile info
    profile_info = load_profile(profile)

    # -- prepare prompt
    # arguments
    if last > 0:
        opt = f"--last {last} "
    else:
        opt = ""
    repo = profile_info["repository"]
    # prompt

    prompt = f"borg list {opt}{repo}"

    # -- print and execute
    print(f"[bold blue]Running :[/bold blue] $> {prompt}")
    subprocess.run(prompt, shell=True)


@app.command(rich_help_panel="Configs")
def init():
    """
    [blue]Initializes[/blue] the profile config file.
    """
    # - create config dir
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()

    # - ask confirmation if already profile
    if PROFILES_FILE.is_file():
        msg = f"There is already an existing profile file at '{PROFILES_FILE}', overwrite it ?"
        overwrite = typer.confirm(msg)
        if not overwrite:
            print("Do not overwrite...")
            raise typer.Abort()
        print("Overwriting the file !")

    # - create default config
    config = configparser.ConfigParser(interpolation=None)
    config["example"] = {
        "description": "Save Important in ovh-sbg",
        "sudo": False,
        "source": "/path/to/backup/source",
        "repository": "/path/to/borg/repo",
        "save_fmt": r"{now:%Y-%m-%d_%H:%M:%S}_{hostname}",
        "option": "--exclude-from ~/.config/pyborg/borg-exclude",
        "compression": "lz4,7",
    }

    with PROFILES_FILE.open("+w") as f:
        config.write(f)

    # - print success
    print("Example config file created !")
    print(f">> {PROFILES_FILE}")
