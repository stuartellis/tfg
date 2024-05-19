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


def build_arg_parser(version: str) -> argparse.ArgumentParser:
    """Create the parser for the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generates commands for Terraform and OpenTofu."
    )
    parser.add_argument(
        "-v",
        "--version",
        help="show the version of this script and exit",
        action="version",
        version="%(prog)s " + version,
    )
    return parser


def main() -> None:
    """Run with command-line options."""
    parser = build_arg_parser(version=VERSION)
    opts = vars(parser.parse_args())
    run(opts)


def run(options: dict[str:Any]) -> None:
    """Run."""
    if len(options) > 0:
        print(options)
    else:
        sys.stderr.write("Arguments are required")
        sys.exit(1)

"""Run the main() function when this file is executed"""
if __name__ == "__main__":
    main()
