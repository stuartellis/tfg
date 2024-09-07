<!--
SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT
-->

# Contributing to This Project

## Table of Contents

- [Preparing a Development Environment](#preparing-a-development-environment)
- [Using the Tasks](#using-the-tasks)
- [Testing](#testing)
- [Documentation](#documentation)
- [Commit Messages](#commit-messages)
- [Versioning](#versioning)
- [Licenses](#licenses)

## Preparing a Development Environment

### Requirements

You may develop this project with macOS or any Linux system, including a WSL environment. The system must have these tools installed:

- [Git](https://www.git-scm.com/)
- [pre-commit](https://pre-commit.com)
- [Python 3.10 or above](https://www.python.org/)
- [Task](https://taskfile.dev/)
- [Trivy](https://aquasecurity.github.io/trivy)

This project includes a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) configuration to provide a development environment in Visual Studio Code. This Dev Container configuration includes the required tools.

### Setting Up The Project

1. Ensure that you have the [required tools](#requirements).
2. Run the task in this project to set up the environment:

```shell
task setup
```

## Using the Tasks

This project includes sets of tasks. To see a list of the available tasks, type *task* in a terminal window:

```shell
task
```

### Standard Tasks

This project provides these tasks:

```shell
* build:         Build artifacts
* clean:         Delete generated files for project
* docs:          Run Website for project documentation
* fmt:           Format code         (aliases: format)
* lint:          Run all checks      (aliases: check)
* list:          List available tasks
* setup:         Set up environment for development      (aliases: bootstrap)
* test:          Run tests
* upgrade:       Upgrade requirements files
* version:       Get current project version
```

## Testing

To run the tests for this project, use this command:

```shell
task test
```

This runs the [pre-commit](https://pre-commit.com/) checks before it runs the test suite. This ensures that the project remains in a consistent working state.

## Documentation

This project follows the [Standard README](https://github.com/RichardLitt/standard-readme) specification for the README file. Documentation is handled by [mkdocs](https://www.mkdocs.org).

The *mkdocs* configuration requires the project to be installed in Python editable mode. To ensure that the project is installed in editable mode, run the *setup* task:

```shell
task setup
```

To view the documentation for this project in your Web browser, run this command:

```shell
task docs
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

For example, to create tag *v0.3.0* with the comment *Release for 202407010931z*, run these commands:

```shell
git checkout main
git tag -am "Release for 202407010931z" v0.3.0
git push --tags
```

## Licenses

This project is licensed under the [MIT](https://spdx.org/licenses/MIT.html) license © 2024-present Stuart Ellis.

Some configuration files in this project are licensed under the [Creative Commons Zero v1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license. Each of these files has the [SPDX](https://spdx.dev) license identifier *CC0-1.0* either at the top of the file or in a *.license* file that has the same name as the file to be licensed.

This project is compliant with [version 3.2 of the REUSE Specification](https://reuse.software/spec/).
