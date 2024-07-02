# SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>
#
# SPDX-License-Identifier: MIT

"""
Logging module for the TFG application.

This module provides logging for the application.
"""

import logging.config

_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def setup_logging(level: str) -> None:
    """
    Configure logging.

    Parameters
    ----------
    level: str
           Log level.

    Returns
    -------
    None
        Does not return a value.

    Raises
    ------
    None

    """
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "human_readable": {
                "format": "%(asctime)s %(levelname)s: %(message)s",
                "datefmt": _DATE_FORMAT,
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "human_readable",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "root": {
                "level": level,
                "handlers": [
                    "stdout",
                ],
            },
        },
    }
    logging.config.dictConfig(config=logging_config)
