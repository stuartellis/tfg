#!/usr/bin/env python3

"""
Command-line interface for tfg.

SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT

"""

# Disable check for line-length
# ruff: noqa: E501

import argparse
import json
import subprocess
import sys
from importlib.metadata import version
from os import environ
from pathlib import Path
from string import Template
from typing import Any

import config
import context


def cli() -> None:
    """Run with command-line options."""
    version_id = get_version()
    parser = build_arg_parser(
        version=version_id, subcommands=[*config.TEMPLATE_SUB_COMMANDS]
    )
    opts = vars(parser.parse_args())
    run(opts)


def build_arg_parser(version: str, subcommands: list[str]) -> argparse.ArgumentParser:
    """Create the parser for the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generates commands for Terraform and OpenTofu."
    )
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
        version=f"%(prog)s {version}",
    )
    return parser


def build_config() -> dict[Any, Any]:
    """Build the full configuration object."""
    env_vars = get_env_vars(config.REQUIRED_VARS, config.OPTIONAL_VARS)
    missing_vars = check_env_vars(env_vars, config.REQUIRED_VARS)
    if len(missing_vars) > 0:
        print(f"Missing required variables: {', '.join(missing_vars)}")
        sys.exit(1)

    project_root_dir = Path.cwd()
    path_set = context.build_path_set(
        project_root_dir, env_vars["ENVIRONMENT"], env_vars["STACK_NAME"]
    )

    config_dict = context.build_config_dict(env_vars, path_set)

    if "variant" not in config_dict:
        config_dict["variant"] = "default"

    return config_dict


def check_env_vars(env_vars: dict[str, str], required_vars: list[str]) -> list[str]:
    """Return all of the required variables that are not present."""
    return [r_var for r_var in required_vars if r_var not in env_vars]


def execute_cmd_string(cmd: str) -> subprocess.CompletedProcess:
    """Execute the command."""
    return subprocess.run(cmd, check=True, shell=True)  # noqa: S602


def get_env_vars(required_vars: list[str], optional_vars: list[str]) -> dict[str, str]:
    """Return object of environment variables."""
    env_variables = [*required_vars, *optional_vars]
    return {k: v for k, v in environ.items() if k in env_variables}


def info() -> dict[str, str]:
    """Summary of active environment."""
    python_version = [
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    ]

    return {
        "python_version": ".".join([str(v) for v in python_version]),
        "tf_exe": context.tf_exe(config.TF_EXES),
        "tfg_version": get_version(),
    }


def load_json(file_path: Path) -> Any:  # noqa: ANN401
    """Return variables from JSON."""
    with Path.open(file_path) as f_in:
        return json.load(f_in)


def print_debug_info(options: dict[str, Any], context: dict[str, Any]) -> None:
    """Output debug info."""
    print(f"Options: {options}")
    print(f"Environment: {info()}")
    print(f"Context: {context}")


def render_cmd_string(context: dict[str, Any], template: str) -> str:
    """Return string for command."""
    return Template(template).substitute(context)


def run(options: dict[str, Any]) -> None:
    """Run."""
    if not options["subcommand"]:
        sys.stderr.write("Arguments are required")
        sys.exit(1)
    else:
        payload = build_config()
        cmd_context = context.tf_context(payload, config.TF_EXES)

        if options["debug"]:
            print_debug_info(options, cmd_context)

        if options["subcommand"] in config.TEMPLATE_SUB_COMMANDS:
            template = config.TEMPLATE_SUB_COMMANDS[options["subcommand"]]
            cmd = render_cmd_string(cmd_context, template)

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


def get_version() -> str:
    """Return version."""
    return version(__package__)


"""Run the main() function when this file is executed"""
if __name__ == "__main__":
    cli()
