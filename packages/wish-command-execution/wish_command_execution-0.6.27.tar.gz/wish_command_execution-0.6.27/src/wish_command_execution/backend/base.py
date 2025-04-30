"""Base backend interface for command execution."""

from wish_models import Wish
from wish_models.system_info import SystemInfo


class Backend:
    """Base class for command execution backends."""

    async def execute_command(self, wish: Wish, command: str, cmd_num: int, log_files, timeout_sec: int) -> None:
        """Execute a command for a wish.

        Args:
            wish: The wish to execute the command for.
            command: The command to execute.
            cmd_num: The command number.
            log_files: The log files to write output to.
            timeout_sec: The timeout in seconds for this command.
        """
        raise NotImplementedError

    async def check_running_commands(self):
        """Check status of running commands and update their status."""
        raise NotImplementedError

    async def cancel_command(self, wish: Wish, cmd_num: int) -> str:
        """Cancel a running command.

        Args:
            wish: The wish to cancel the command for.
            cmd_num: The command number to cancel.

        Returns:
            A message indicating the result of the cancellation.
        """
        raise NotImplementedError

    async def get_system_info(self) -> SystemInfo:
        """Get system information.

        Returns:
            SystemInfo: Collected system information
        """
        raise NotImplementedError
