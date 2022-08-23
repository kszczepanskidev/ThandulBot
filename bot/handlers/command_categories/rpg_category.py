from discord.ext import commands

from ..helpers import remove_command_message, should_perform_command, should_perform_gm_command, reminder_loop
from ..command_handlers.add_dates_command import add_dates_command
from ..command_handlers.check_dates_command import check_dates_command
from ..command_handlers.append_dates_command import append_dates_command

class RPGCommands(commands.Cog):
    running_task = None

    """
    Commands that helps in organising RPG Tabletop game sessions.
    Messages with command are removed.
    Usable only in channels and by users specified in environment configuration.
    """

    @commands.command(name='addDates')
    async def add_dates(self, context, dates, *args):
        """
        Posts embed message with dates for players to vote for with corresponding reactions.

        Parameters:
            - dates: list of dates for poll in `%d.%m` format, separated with semicolon.
            - args: collection of strings that will create custom message to be put as custom title above dates list.

        Removes message with command.
        Usable only in channels and by game masters specified in environment configuration.
        """
        await remove_command_message(context.message)

        if not should_perform_gm_command(context):
            return

        await add_dates_command(context, dates, ' '.join(args))

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

    @commands.command(name='appendDates')
    async def append_dates(self, context, message, dates):
        """
        Edits given message by appending new dates.

        Removes message with command.
        Usable only in channels and by users specified in environment configuration.
        """
        await remove_command_message(context.message)

        if not should_perform_command(context):
            return

        await append_dates_command(context, message, dates)

    @commands.command(name='startReminder')
    async def startUserReminder(self, context, user, *args):
        """
        Begins reminder loop to send a message daily to given user.

        Usable only by users specified in environment configuration.
        """

        if not should_perform_command(context):
            return

        if self.running_task != None:
            reminder_loop.restart(context, user, ' '.join(args))
        else:
            self.running_task = reminder_loop.start(context, user, ' '.join(args))

    @commands.command(name='stopReminder')
    async def stopUserReminder(self, context):
        """
        Stops reminder loops that send a message daily to given user.

        Usable only by users specified in environment configuration.
        """

        if not should_perform_command(context):
            return

        reminder_loop.cancel()
