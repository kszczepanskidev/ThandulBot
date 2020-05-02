from discord.ext import commands

from ..helpers import should_perform_command
from ..command_handlers.message_command import send_message_command

class AdminCommands(commands.Cog):
    """
    Commands that perform some advanced steps.

    Usable only in channels specified in environment configuration.
    """

    @commands.command(name='message')
    async def message(self, context, *args):
        """
        Sends message to a channel.

        Parameters:
            - channel: id of channel to which message should be sent.
            - text: text of message to send. For mentions use <@&role_id> or <@user_id>. For emoji use <:emoji_name:emoji_id>

        Usable only in channels specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await send_message_command(context, args)