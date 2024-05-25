#!/usr/bin/env python3

"""
tfg generates commands for Terraform and OpenTofu.

SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT
"""

import argparse
import sys
from typing import Any

VERSION = "0.1.0"

SUB_COMMANDS = [
    "apply",
    "fmt",
    "destroy",
    "info",
    "init",
    "plan",
    "status",
    "validate",
]


def build_arg_parser(version: str, subcommands: list[str]) -> argparse.ArgumentParser:
    """Create the parser for the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generates commands for Terraform and OpenTofu."
    )
    parser.add_argument(
        "subcommand",
        choices=subcommands,
        help=f"subcommand to run: {" ".join(subcommands)}",
    )
    parser.add_argument(
        "--debug", help="output the generated context", action="store_true"
    )
    parser.add_argument(
        "-v",
        "--version",
        help="show the version of this script and exit",
        action="version",
        version="%(prog)s " + version,
    )
    return parser


def info() -> dict[str, str]:
    """Summary of active environment."""
    python_version = [
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    ]

    return {
        "python_version": ".".join([str(v) for v in python_version]),
        "tf_exe": tf_exe_name(),
        "tfg_version": VERSION,
    }


def main() -> None:
    """Run with command-line options."""
    parser = build_arg_parser(version=VERSION, subcommands=valid_subcommands())
    opts = vars(parser.parse_args())
    run(opts)


def print_debug_info(options: dict[str, Any]) -> None:
    """Output debug info."""
    print(options)
    print(info())


def run(options: dict[str, Any]) -> None:
    """Run."""
    if options["debug"]:
        print_debug_info(options)
    elif options["subcommand"]:
        print(options["subcommand"])
    else:
        sys.stderr.write("Arguments are required")
        sys.exit(1)


def valid_subcommands() -> list[str]:
    """Return list of subcommands."""
    return SUB_COMMANDS


def tf_exe_name() -> str:
    """Return executable for TF."""
    return "terraform"


"""Run the main() function when this file is executed"""
if __name__ == "__main__":
    main()
