"""
Bundle functions for tfg.

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
        "tf_context_json": tf_root_dir.joinpath(
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


def tf_settings(env_config: dict[str, str], context: Any, tf_exes: list[str]) -> dict[str, str]:
    """Return settings for TF commands."""
    settings = env_config.copy()
    settings["tf_exe"] = tf_exe(tf_exes)

    settings["tf_plan_path"] = pathsep.join(
        [env_config["tf_tmp_dir"], build_tf_plan_name(settings)]
    )
    settings["tf_vars_files_opt"] = build_tf_vars_files_opt(env_config)
    settings["tf_vars_opt"] = build_tf_vars_extras_opt(env_config)

    if tf_remote_backend_required(env_config):
        backend_type = tf_backend_type()
        settings["tf_backend_opts"] = build_tf_remote_backend_opts(
            context, backend_type
        )
    else:
        settings["tf_backend_opts"] = "-backend=false"

    return settings


def tf_exe(tf_names: list[str]) -> str:
    """Return executable for TF."""
    for tf_name in tf_names:
        if which(tf_name):
            return tf_name

    err = f"No TF executable found. Ensure that PATH has one of these: {', '.join(tf_names)}."
    raise FileNotFoundError(err)
