from discord import app_commands, Interaction

from ..helpers import should_perform_command
from ..command_handlers.weather_command import weather_command

class Information(app_commands.Group):
    """
    Commands that post information fetched from external API.

    Removes message with command.
    Usable only in channels specified in environment configuration.
    """

    @app_commands.command(name='weather')
    @app_commands.describe(city='name of city for which weather should be fetched.')
    async def weather(self, interaction: Interaction, city: str):
        """
        Posts embed message with weather for given city.

        Parameters:
            - city: name of city for which weather should be fetched.

        Removes message with command.
        Usable only in channels specified in environment configuration.
        """

        if not should_perform_command(interaction):
            return

        await weather_command(interaction, city)
