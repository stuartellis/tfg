#!/usr/bin/env python3

"""
tfg generates commands for Terraform.

This script requires Python 3.10 or above. It has no other dependencies.

Usage:

    ./tfg.py version

Help:

    ./tfg.py --help

It is provided under the terms of the MIT License:

SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT

"""

import argparse
import subprocess
import sys
from os import environ
from string import Template
from typing import Any

VERSION = "0.1.0"

ENV_VARS = ["PWD"]

SUB_COMMANDS = {
    "apply": "",
    "fmt": "",
    "destroy": "",
    "init": "",
    "plan": "",
    "status": "",
    "validate": "",
    "version": "$tf_exe version",
}


def build_arg_parser(version: str, subcommands: list[str]) -> argparse.ArgumentParser:
    """Create the parser for the command-line arguments."""
    parser = argparse.ArgumentParser(description="Generates commands for Terraform.")
    parser.add_argument(
        "subcommand",
        choices=subcommands,
        help=f"subcommand to run: {subcommands}",
    )
    parser.add_argument(
        "-d", "--debug", help="output the generated context", action="store_true"
    )
    parser.add_argument(
        "-p",
        "--print",
        help="output the command without executing it",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="show the version of this script and exit",
        action="version",
        version="%(prog)s " + version,
    )
    return parser


def build_context() -> dict[str, str]:
    """Return context object for templates."""
    exe_vars = {"tf_exe": tf_exe_name()}
    env_vars = {k.lower(): v for k, v in environ.items() if k in ENV_VARS}
    return {**exe_vars, **env_vars}


def execute_cmd_string(cmd: str) -> subprocess.CompletedProcess:
    """Execute the command."""
    return subprocess.run(cmd, check=True, shell=True)  # noqa: S602


def info() -> dict[str, str]:
    """Summary of active environment."""
    python_version = [
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    ]

    return {
        "python_version": ".".join([str(v) for v in python_version]),
        "tf_exe_name": tf_exe_name(),
        "tfg_version": VERSION,
    }


def main() -> None:
    """Run with command-line options."""
    parser = build_arg_parser(version=VERSION, subcommands=[*SUB_COMMANDS])
    opts = vars(parser.parse_args())
    run(opts)


def print_debug_info(options: dict[str, Any], context: dict[str, Any]) -> None:
    """Output debug info."""
    print(f"Options: {options}")
    print(f"Environment: {info()}")
    print(f"Context: {context}")


def render_cmd_string(context: dict[str, str], template: str) -> str:
    """Return string for command."""
    return Template(template).substitute(context)


def run(options: dict[str, Any]) -> None:
    """Run."""
    if options["subcommand"]:
        context = build_context()

        if options["debug"]:
            print_debug_info(options, context)

        template = SUB_COMMANDS[options["subcommand"]]
        cmd = render_cmd_string(context, template)

        if options["print"]:
            print(cmd)
        else:
            try:
                execute_cmd_string(cmd)
            except FileNotFoundError as exc:
                print(
                    f"Process failed because the executable could not be found.\n{exc}"
                )
            except subprocess.CalledProcessError as exc:
                print(
                    f"Process failed because did not return a successful return code. "
                    f"Returned {exc.returncode}\n{exc}"
                )
    else:
        sys.stderr.write("Arguments are required")
        sys.exit(1)


def tf_exe_name() -> str:
    """Return executable for TF."""
    return "terraform"


"""Run the main() function when this file is executed"""
if __name__ == "__main__":
    main()
