#!/usr/bin/env python3

"""
tfg generates commands for Terraform.

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
from os import environ, pathsep
from pathlib import Path
from shutil import which
from string import Template
from typing import Any

## Constants

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
    "apply": "$tf_exe -chdir=$tf_def_dir apply -auto-approve $tf_plan_path",
    "check": "$tf_exe -chdir=$tf_def_dir fmt -check -diff -recursive",
    "fmt": "$tf_exe -chdir=$tf_def_dir fmt -recursive",
    "destroy": "$tf_exe -chdir=$tf_def_dir apply -destroy -auto-approve $tf_vars_opt $tf_vars_files_opt",
    "forget": "$tf_exe -chdir=$tf_def_dir apply workspace delete $variant",
    "init": "$tf_exe -chdir=$tf_def_dir init $tf_backend_opts",
    "plan": "$tf_exe -chdir=$tf_def_dir plan -out=$tf_plan_path $tf_vars_opt $tf_vars_files_opt",
    "show": "$tf_exe -chdir=$tf_def_dir show -json",
    "test": "$tf_exe -chdir=$tf_def_dir test $tf_vars_opt $tf_vars_files_opt",
    "validate": "$tf_exe -chdir=$tf_def_dir validate",
    "version": "$tf_exe version",
}

TF_EXES = ["terraform", "tofu"]

## Functions for template context


def build_config_dict(
    env_vars: dict[str, str],
    path_set: dict[str, Path],
) -> dict[str, str]:
    """Build configuration object."""
    env_vars = {k.lower(): v for k, v in env_vars.items()}
    paths = {p: str(v) for p, v in path_set.items()}
    return {**env_vars, **paths}


def build_path_set(root_dir: Path, environment: str, stack: str) -> dict[str, Path]:
    """Return a dictionary of the required paths."""
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
        "tf_tmp_dir": tf_root_dir.joinpath("tmp").absolute(),
    }


def build_tf_remote_backend_opts(document: Any, backend_type: str) -> str:  # noqa: ANN401
    """Return remote backend options for TF."""
    config = document[backend_type]
    opts = [f"-backend-config={opt}={config[opt]}" for opt in config]
    opts.append("-backend-config=workspace_key_prefix=workspaces")
    return " ".join(opts)


def build_tf_plan_name(config: dict[str, str]) -> str:
    """Return name of plan file for TF."""
    return f"{config['environment']}-{config['stack_name']}-{config['variant']}.tfplan"


def build_tf_vars_files_opt(config: dict[str, str]) -> str:
    """Return var files for TF."""
    return f"-var-file={config['tf_envs_dir']}/all/{config['stack_name']}.tfvars -var-file={config['tf_env_dir']}/{config['stack_name']}.tfvars"


def build_tf_vars_extras_opt(config: dict[str, str]) -> str:
    """Return extra vars for TF."""
    names = ["environment", "stack_name", "variant"]
    opts = [f"-vars={name}={config[name]}" for name in names]
    return " ".join(opts)


def tf_remote_backend_required(config: dict[str, str]) -> bool:
    """Specify if a TF remote backend is required."""
    if "st_enable_backend" in config and config["st_enable_backend"].lower() == "true":
        return True
    return not (
        "st_enable_backend" in config and config["st_enable_backend"].lower() == "false"
    )


def tf_backend_type() -> str:
    """Return current backend type for TF."""
    return "aws"


def tf_context(config: dict[str, str]) -> dict[str, str]:
    """Return context for TF commands."""
    context = config.copy()
    context["tf_exe"] = tf_exe(TF_EXES)

    context["tf_plan_path"] = pathsep.join(
        [config["tf_tmp_dir"], build_tf_plan_name(context)]
    )
    context["tf_vars_files_opt"] = build_tf_vars_files_opt(config)
    context["tf_vars_opt"] = build_tf_vars_extras_opt(config)

    if tf_remote_backend_required(config):
        backend_type = tf_backend_type()
        tf_backend_document = load_json(Path(context["tf_backend_json"]))
        context["tf_backend_opts"] = build_tf_remote_backend_opts(
            tf_backend_document, backend_type
        )
    else:
        context["tf_backend_opts"] = "-backend=false"

    return context


def tf_exe(tf_names: list[str]) -> str:
    """Return executable for TF."""
    for tf_name in tf_names:
        if which(tf_name):
            return tf_name

    err = f"No TF executable found. Ensure that PATH has one of these: {', '.join(tf_names)}."
    raise FileNotFoundError(err)


### Functions for command-line


def cli() -> None:
    """Run with command-line options."""
    version_id = get_version()
    parser = build_arg_parser(version=version_id, subcommands=[*TEMPLATE_SUB_COMMANDS])
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
    env_vars = get_env_vars(REQUIRED_VARS, OPTIONAL_VARS)
    missing_vars = check_env_vars(env_vars, REQUIRED_VARS)
    if len(missing_vars) > 0:
        print(f"Missing required variables: {', '.join(missing_vars)}")
        sys.exit(1)

    project_root_dir = Path.cwd()
    path_set = build_path_set(
        project_root_dir, env_vars["ENVIRONMENT"], env_vars["STACK_NAME"]
    )

    config = build_config_dict(env_vars, path_set)

    if "variant" not in config:
        config["variant"] = "default"

    return config


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
        "tf_exe": tf_exe(TF_EXES),
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
        config = build_config()
        cmd_context = tf_context(config)

        if options["debug"]:
            print_debug_info(options, cmd_context)

        if options["subcommand"] in TEMPLATE_SUB_COMMANDS:
            template = TEMPLATE_SUB_COMMANDS[options["subcommand"]]
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
