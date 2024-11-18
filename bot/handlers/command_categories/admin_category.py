from discord import app_commands, Interaction
from typing import Optional

from ..helpers import should_perform_command, should_perform_foundry_admin_command
from ..command_handlers.message_command import send_message_command
from ..command_handlers.restart_foundry_command import restart_foundry_command

class AdminCommands(app_commands.Group):
    """
    Commands that perform some advanced steps.

    Usable only in channels specified in environment configuration.
    """

    @app_commands.command(name='message')
    @app_commands.describe(channel='id of channel to which message should be sent.')
    @app_commands.describe(message='text of message to send. For mentions use <@&role_id> or <@user_id>. For emoji use <:emoji_name:emoji_id>')
    async def message(self, interaction: Interaction, channel: str, message: str):
        """
        Sends message to a channel.

        Parameters:
            - channel: id of channel to which message should be sent.
            - message: text of message to send. For mentions use <@&role_id> or <@user_id>. For emoji use <:emoji_name:emoji_id>

        Usable only in channels specified in environment configuration.
        """
        if not should_perform_command(interaction):
            return

        await send_message_command(interaction, channel, message)

    @app_commands.command(name='restart-foundry')
    @app_commands.describe(instance='optional name of instance to restart (in case of running multiple instances as one user)')
    async def restart_foundry(self, interaction: Interaction, instance: Optional[str] = None):
        """
        Restarts Foundry VTT instance for invoking GM.

        Parameters:
            - instance: id of channel to which message should be sent.

        Usable only in by Foundry VTT admins with specified instances.
        """
        if not should_perform_foundry_admin_command(interaction):
            return

        await restart_foundry_command(interaction, instance)
