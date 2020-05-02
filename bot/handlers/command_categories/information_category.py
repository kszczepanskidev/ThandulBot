from discord.ext import commands

from ..helpers import remove_command_message, should_perform_command
from ..command_handlers.weather_command import weather_command

class Information(commands.Cog):
    """
    Commands that post information fetched from external API.

    Removes message with command.
    Usable only in channels specified in environment configuration.
    """

    @commands.command(name='weather')
    async def weather(self, context, *args):
        """
        Posts embed message with weather for given city.

        Parameters:
            - city name: name of city for which weather should be fetched.

        Removes message with command. 
        Usable only in channels specified in environment configuration.
        """
        await remove_command_message(context.message)

        if len(args) == 0:
            return

        if not should_perform_command(context):
            return

        city = ' '.join(args)
        await weather_command(context, city)