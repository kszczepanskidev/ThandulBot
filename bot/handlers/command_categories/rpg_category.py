from discord import app_commands, Interaction
from typing import Optional

from ..helpers import should_perform_command, should_perform_gm_command
from ..command_handlers.add_dates_command import add_dates_command
from ..command_handlers.append_dates_command import append_dates_command

class RPGCommands(app_commands.Group):
    """
    Commands that helps in organizing RPG Tabletop game sessions.
    Messages with command are removed.
    Usable only in channels and by users specified in environment configuration.
    """

    @app_commands.command(name='add-dates')
    @app_commands.describe(dates='dates for poll in list (`%d.%m;%d.%m`) or range (`%d.%m-%d.%m`) format.')
    @app_commands.describe(title='optional text to be put as custom title above dates list.')
    async def add_dates(self, interaction: Interaction, dates: str, title: Optional[str] = None):
        """
        Posts embed message with dates for players to vote for with corresponding reactions.

        Parameters:
            - dates: dates for poll in list (`%d.%m;%d.%m`) or range (`%d.%m-%d.%m`) format.
            - title: optional text to be put as custom title above dates list.

        Removes message with command.
        Usable only in channels and by game masters specified in environment configuration.
        """

        if not should_perform_gm_command(interaction):
            return

        await add_dates_command(interaction, dates, title)

    @app_commands.command(name='append-dates')
    @app_commands.describe(message='id of message to appends dates to.')
    @app_commands.describe(dates='dates for poll in list (`%d.%m;%d.%m`) or range (`%d.%m-%d.%m`) format.')
    async def append_dates(self, interaction: Interaction, message: str, dates: str):
        """
        Edits given message by appending new dates.

        Parameters:
            - message: id of message to appends dates to.
            - dates: dates for poll in list (`%d.%m;%d.%m`) or range (`%d.%m-%d.%m`) format.

        Removes message with command.
        Usable only in channels and by users specified in environment configuration.
        """

        if not should_perform_command(interaction):
            return

        await append_dates_command(interaction, message, dates)
