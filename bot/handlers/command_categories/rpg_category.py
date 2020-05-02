from discord.ext import commands

from ..helpers import remove_command_message, should_perform_command
from ..command_handlers.add_dates_command import add_dates_command
from ..command_handlers.check_dates_command import check_dates_command

class RPGCommands(commands.Cog):
    """
    Commands that helps in organising RPG Tabletop game sessions.
    Messages with command are removed. 
    Usable only in channels and by users specified in environment configuration.
    """

    @commands.command(name='addDates')
    async def add_dates(self, context, dates):
        """
        Posts embed message with dates for players to vote for with corresponding reactions.

        Parameters:
            - dates: list of dates for poll in `%d.%m` format, separated with semicolon.

        Removes message with command. 
        Usable only in channels and by users specified in environment configuration.
        """
        await remove_command_message(context.message)

        if not should_perform_command(context):
            return

        await add_dates_command(context, dates)

    @commands.command(name='twat')
    async def check_dates(self, context):
        """
        Checks last posted dates poll and posts message that depends on votes:
            - ping users that didn't vote yet.
            - lists dates with votes from all users.
            - posts sad message when there is no date with reaction from all users.
        Users list for this check is specified in environment configuration.

        Removes message with command.
        Usable only in channels and by users specified in environment configuration.
        """
        await remove_command_message(context.message)

        if not should_perform_command(context):
            return

        await check_dates_command(context)