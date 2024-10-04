"""
Config for tfg.

SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT

"""

# Disable check for line-length
# ruff: noqa: E501

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
