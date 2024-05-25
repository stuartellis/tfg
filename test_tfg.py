"""
Tests for tfg.

SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT
"""

import pytest
import tfg

## Tests for command-line


def test_no_subcommand(capsys: pytest.CaptureFixture[str]) -> None:
    """Exit when called with no subcommand."""
    with pytest.raises(SystemExit):
        tfg.run({"debug": False, "subcommand": None,})
    captured = capsys.readouterr()
    assert "Arguments are required" in captured.err


## Tests for functions


def test_info_contains_tfg_version() -> None:
    """Info dictionary contains tfg version."""
    info = tfg.info()
    assert info["tfg_version"] == tfg.VERSION


def test_tf_exe_is_valid() -> None:
    """Function returns valid executable name."""
    tf_exe_name = tfg.tf_exe_name()
    assert tf_exe_name in ["terraform", "tofu"]
