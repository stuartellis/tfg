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
import json
import subprocess
import sys
from os import environ
from pathlib import Path
from string import Template
from typing import Any

VERSION = "0.1.0"

REQUIRED_VARS = [
    "ENVIRONMENT",
    "STACK_NAME",
]

OPTIONAL_VARS = [
    "ST_ENABLE_BACKEND",
    "ST_RUN_CONTAINER",
    "VARIANT",
]

TEMPLATE_SUB_COMMANDS = {
    "apply": "",
    "fmt": "",
    "destroy": "",
    "init": "",
    "plan": "",
    "validate": "",
    "version": "$tf_exe version",
}

TF_BACKEND_MODE = "aws"


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


def build_context(
    host_vars: dict[str, str],
    tf_backend_vars: dict[str, str],
    env_vars: dict[str, str],
    path_set: dict[str, Path],
) -> dict[str, str]:
    """Build context object."""
    env_vars = {k.lower(): v for k, v in env_vars.items()}
    paths = {p: str(v) for p, v in path_set.items()}
    return {**host_vars, **tf_backend_vars, **env_vars, **paths}


def build_env_vars(
    required_vars: list[str], optional_vars: list[str]
) -> dict[str, str]:
    """Return object of environment variables for templates."""
    env_variables = [*required_vars, *optional_vars]
    return {k: v for k, v in environ.items() if k in env_variables}


def build_path_set(root_dir: Path, environment: str, stack: str) -> dict[str, Path]:
    """Return paths."""
    tf_root_dir = root_dir.joinpath("terraform1", "stacks")
    return {
        "project_dir": root_dir.absolute(),
        "tf_defs_dir": tf_root_dir.joinpath("definitions").absolute(),
        "tf_def_dir": tf_root_dir.joinpath("definitions", stack).absolute(),
        "tf_envs_dir": tf_root_dir.joinpath("environments").absolute(),
        "tf_env_dir": tf_root_dir.joinpath("environments", environment).absolute(),
        "tf_backend_json": tf_root_dir.joinpath(
            "environments", environment, "backend.json"
        ).absolute(),
        "tf_modules_dir": tf_root_dir.joinpath("modules").absolute(),
    }


def build_tf_backend_opt(context: dict[str, str]) -> str:
    """Return backend options for TF."""
    opts = [f"-backend-config={opt}={context[opt]}" for opt in context]
    return " ".join(opts)


def tf_backend_required(context: dict[str, str]) -> bool:
    """Specify if a TF remote backend is required."""
    if (
        "st_enable_backend" in context
        and context["st_enable_backend"].lower() == "true"
    ):
        return True
    return not (
        "st_enable_backend" in context
        and context["st_enable_backend"].lower() == "false"
    )


def check_env_vars(env_vars: dict[str, str], required_vars: list[str]) -> list[str]:
    """Return all of the required variables that are not present."""
    return [r_var for r_var in required_vars if r_var not in env_vars]


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
        "tf_exe": tf_exe(),
        "tfg_version": VERSION,
    }


def load_json(file_path: Path) -> Any:  # noqa: ANN401
    """Return variables from JSON."""
    with Path.open(file_path) as f_in:
        return json.load(f_in)


def main() -> None:
    """Run with command-line options."""
    parser = build_arg_parser(version=VERSION, subcommands=[*TEMPLATE_SUB_COMMANDS])
    opts = vars(parser.parse_args())
    run(opts)


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
    if options["subcommand"]:
        env_vars = build_env_vars(REQUIRED_VARS, OPTIONAL_VARS)
        missing_vars = check_env_vars(env_vars, REQUIRED_VARS)
        if len(missing_vars) > 0:
            print(f"Missing required variables: {', '.join(missing_vars)}")
            sys.exit(1)

        project_root_dir = Path.cwd()
        path_set = build_path_set(
            project_root_dir, env_vars["ENVIRONMENT"], env_vars["STACK_NAME"]
        )
        tf_backend_vars = load_json(path_set["tf_backend_json"])
        host_vars = {"tf_exe": tf_exe()}
        context: dict[str, Any] = build_context(
            host_vars, tf_backend_vars, env_vars, path_set
        )

        if tf_backend_required(context):
            context["tf_backend_opt"] = build_tf_backend_opt(context[TF_BACKEND_MODE])
        else:
            context["tf_backend_opt"] = "-backend=false"

        if options["debug"]:
            print_debug_info(options, context)

        template = TEMPLATE_SUB_COMMANDS[options["subcommand"]]
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


def tf_exe() -> str:
    """Return executable for TF."""
    return "terraform"


"""Run the main() function when this file is executed"""
if __name__ == "__main__":
    main()
