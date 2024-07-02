# SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>
#
# SPDX-License-Identifier: MIT

"""
Configuration module for the TFG application.

This module provides configuration for the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class.

    Uses Pydantic Settings.
    """

    model_config = SettingsConfigDict(env_prefix="CANO_")
    dry_run: bool = False
    log_level: str = "INFO"
