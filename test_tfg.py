"""
Tests for tfg.

SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>

SPDX-License-Identifier: MIT
"""

import pytest
import tfg


def test_no_args(capsys: pytest.CaptureFixture[str]) -> None:
    """Exit when called with no arguments."""
    with pytest.raises(SystemExit):
        tfg.run([])
    captured = capsys.readouterr()
    assert "Arguments are required" in captured.err
