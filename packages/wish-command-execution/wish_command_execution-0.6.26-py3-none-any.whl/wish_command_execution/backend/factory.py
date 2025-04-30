"""Factory for creating backends."""

from typing import Union

from pydantic import BaseModel

from wish_command_execution.backend.base import Backend
from wish_command_execution.backend.bash import BashBackend
from wish_command_execution.backend.sliver import SliverBackend


class BashConfig(BaseModel):
    """Configuration for bash backend."""
    shell_path: str = "/bin/bash"


class SliverConfig(BaseModel):
    """Configuration for Sliver backend."""
    session_id: str
    client_config_path: str


def create_backend(config: Union[BashConfig, SliverConfig]) -> Backend:
    """Create a backend based on the configuration.

    Args:
        config: The backend configuration.

    Returns:
        A backend instance.
    """
    if isinstance(config, BashConfig):
        return BashBackend()
    elif isinstance(config, SliverConfig):
        return SliverBackend(config.session_id, config.client_config_path)
    else:
        raise ValueError(f"Unsupported backend configuration: {type(config)}")
