# SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>
#
# SPDX-License-Identifier: MIT

"""
Tests for the command-line module for the TFG application.

This module provides tests for the application.
"""

import contextlib

import pytest

from tfg import app


@pytest.mark.parametrize("option", ["-h", "--help"])
def test_help(capsys: pytest.CaptureFixture[str], option: str) -> None:
    """Test output of help."""
    with contextlib.suppress(SystemExit):
        app.cli([option])
        output = capsys.readouterr().out
        assert "Generates commands for Terraform and OpenTofu." in output
