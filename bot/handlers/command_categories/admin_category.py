from discord import app_commands, Interaction

from ..helpers import should_perform_command
from ..command_handlers.message_command import send_message_command

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
