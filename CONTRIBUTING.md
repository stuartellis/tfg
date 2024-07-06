<!--
SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT
-->

# Contributing to This Project

This project includes a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) configuration to provide a development environment in Visual Studio Code. To use another type of environment, follow the instructions in the [section on preparing a development environment](#preparing-a-development-environment).

> *Tasks:* This project includes sets of tasks for the [Task](https://taskfile.dev/) tool. The Dev Container installs Task and uses it to prepare the development environment.

---

## Table of Contents

- [Preparing a Development Environment](#preparing-a-development-environment)
- [Using the Tasks](#using-the-tasks)
- [Using Container Images](#using-container-images)
- [Testing](#testing)
- [Documentation](#documentation)
- [Commit Messages](#commit-messages)
- [Versioning](#versioning)
- [Licenses](#licenses)

## Preparing a Development Environment

### Requirements

You may develop this project with macOS or any Linux system, including a WSL environment. The system must have these tools installed:

- [Git](https://www.git-scm.com/)
- [Task](https://taskfile.dev/)
- [Python 3.12 or above](https://www.python.org/)
- [pipx](https://pipx.pypa.io/)

> *Microsoft Windows:* Use the Dev Container to develop this project on Microsoft Windows.

### Setting Up The Project

Once you have the necessary tools, run the task in this project to set up environments for development and tests:

```shell
task bootstrap
```

## Using the Tasks

This project includes sets of tasks. To see a list of the available tasks, type *task* in a terminal window:

```shell
task
```

### Standard Tasks

This project provides these tasks:

```shell
* bootstrap:               Set up environment for development      (aliases: setup)
* clean:                   Delete generated files for project
* docs:                    Run Website for project documentation
* fmt:                     Format code         (aliases: format)
* lint:                    Run all checks      (aliases: check)
* list:                    List available tasks
* test:                    Run tests
* update:                  Update project dependencies
* version:                 Get current project version
```

Use the top-level tasks for normal operations. These call the appropriate tasks in the namespaces in the correct order.

### Tasks in the Namespaces

You may run a task in a namespace:

```shell
* py:lint:check:           Run ruff checks                             (aliases: py:lint:lint, py:lint:run)
* py:lint:fmt:             Run ruff formatter with import sorting      (aliases: py:lint:format)
* py:test:typehints:       Run mypy
* py:test:unit:            Run pytest
* venv:compile:            Compile Python requirements files
* venv:create:             Create Python virtual environment
* venv:delete:             Delete Python virtual environment
* venv:editable:           Install as editable to Python virtual environment
```

To run one of the tasks in a namespace, specify the namespace and the task, separated by *:* characters. For example, to run the *check* task in the *py:lint* namespace, enter this command:

```shell
task py:lint:check
```

## Testing

To run the tests for this project, use this command:

```shell
task test
```

This runs [pre-commit](https://pre-commit.com/) with the checks that are defined for the project before it runs the test suite.

To produce a test coverage report for this project, use this command:

## Documentation

This project follows the [Standard README](https://github.com/RichardLitt/standard-readme) specification for the README file. Documentation is handled by [mkdocs](https://www.mkdocs.org).

The *mkdocs* configuration requires the project to be installed in Python editable mode:

```shell
task venv:editable
```

To build the documentation for this project, run this command:

```shell
task doc:build
```

To view the documentation for this project in your Web browser, run this command:

```shell
task docs
```

## Using Container Images

To build a container image for this project, use this command:

```shell
task build
```

Use the *containers* tasks:

```shell
* containers:build:         Build container image
* containers:lint:          Check container build file with Trivy
* containers:rebuild:       Force a complete rebuild of container image
* containers:run:           Run container image
* containers:scan:          Scan container image
* containers:shell:         Open shell in container image
```

## Commit Messages

This project uses the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format for commit messages.

## Versioning

This project uses [Semantic Versioning 2.0](https://semver.org/spec/v2.0.0.html).

The version is automatically calculated from Git tags, using [setuptools_scm](https://setuptools-scm.readthedocs.io).

To see the current version of your copy of the project, run the *version* task:

```shell
task version
```

## Setting a New Version

To raise the version number for the project, add a Git tag that follows the format of [Semantic Versioning 2.0](https://semver.org/spec/v2.0.0.html).

For example, to create version *0.3.0* with the comment *Release for 202407010931z*, run these commands:

```shell
git checkout main
git tag -am "Release for 202407010931z" 0.3.0
git push --tags
```

## Licenses

This project is licensed under the [MIT](https://spdx.org/licenses/MIT.html) license © 2024-present Stuart Ellis.

Some configuration files in this project are licensed under the [Creative Commons Zero v1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license. Each of these files has the [SPDX](https://spdx.dev) license identifier *CC0-1.0* either at the top of the file or in a *.license* file that has the same name as the file to be licensed.

This project is compliant with [version 3.2 of the REUSE Specification](https://reuse.software/spec/).
