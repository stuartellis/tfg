#!/usr/bin/env python3

"""tfg generates commands for Terraform and OpenTofu."""

import argparse

VERSION = '0.1.0'


def build_arg_parser(version: str) -> argparse.ArgumentParser:
    """Create the parser for the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generates commands for Terraform and OpenTofu."
    )
    parser.add_argument(
        '-v', '--version',
        help='show the version of this script and exit',
        action='version', version="%(prog)s " + version)
    return parser


def main() -> None:
    """Build a list of commands."""
    parser = build_arg_parser(version=VERSION)
    vars(parser.parse_args())


"""Runs the main() function when this file is executed"""
if __name__ == "__main__":
    main()
