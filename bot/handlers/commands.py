from discord.ext import commands

from ..environment import bot_environment
from .helpers import remove_command_message, should_perform_command
from .command_handlers.check_dates_command import check_dates_command
from .command_handlers.add_dates_command import add_dates_command
from .command_handlers.weather_command import weather_command
from .command_handlers.animals_commands import post_animal_command, post_random_animal_command
from .command_handlers.help_command import send_help_command
from.command_handlers.message_command import send_message_command

# Register commands categories.
def bindCommands(bot):
    bot.add_cog(AdminCommands())
    bot.add_cog(RPGCommands())
    bot.add_cog(Information())
    bot.add_cog(AnimalRandomPhotos())

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

class AnimalRandomPhotos(commands.Cog):
    """
    Commands that postrandom photos of animals.
    """

    @commands.command(name='cat')
    async def cat(self, context):
        """
        Posts random photo of a cat.
        """
        await post_animal_command(context, 'cat')

    @commands.command(name='dog')
    async def dog(self, context):
        """
        Posts random photo of a dog.
        """
        await post_animal_command(context, 'dog')

    @commands.command(name='fox')
    async def fox(self, context):
        """
        Posts random photo of a fox.
        """
        await post_animal_command(context, 'fox')

    @commands.command(name='duck')
    async def fox(self, context):
        """
        Posts random photo of a duck..
        """
        await post_animal_command(context, 'duck')

    @commands.command(name='goat')
    async def fox(self, context):
        """
        Posts random photo of a goat.
        """
        await post_animal_command(context, 'goat')

    @commands.command(name='animal')
    async def fox(self, context):
        """
        Posts random photo of an random animal.
        """
        await post_random_animal_command(context)