# SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>
#
# SPDX-License-Identifier: MIT

"""
Runner module for the TFG application.

This module provides the runner for the application.
"""

import logging
import sys
from typing import Any

from tfg import config, log_util

logger = logging.getLogger(__name__)


def handle_exception(exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:  # noqa: ANN401
    """
    Handle exceptions that propagate to the top-level.

    Parameters
    ----------
    exc_type : Any
               Type for exception.
    exc_value : Any
               Value for exception.
    exc_traceback : Any
               Traceback for exception.

    Returns
    -------
    None
        Does not return a value.

    Raises
    ------
    None

    """
    logging.critical(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


sys.excepthook = handle_exception


def run() -> None:
    """
    Print a dummy value.

    Parameters
    ----------
    None

    Returns
    -------
    None
        Does not return a value.

    Raises
    ------
    None

    """
    settings = config.Settings()
    log_util.setup_logging(settings.log_level)
    logging.info("Hello world")
