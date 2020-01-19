from ..environment import bot_environment
from .helpers import remove_command_message, should_perform_command
from .check_dates_command import check_dates_command
from .add_dates_command import add_dates_command
from .weather_command import weather_command

def bindCommands(bot):

    @bot.command(name='addDates')
    async def add_dates(context, dates):
        await remove_command_message(context.message)

        if not should_perform_command(context):
            return

        await add_dates_command(context, dates)

    @bot.command(name='twat')
    async def check_dates(context):
        await remove_command_message(context.message)

        if not should_perform_command(context):
            return

        await check_dates_command(context)

    @bot.command(name='weather')
    async def weather(context, *args):
        await remove_command_message(context.message)

        if len(args) == 0:
            return

        if not should_perform_command(context):
            return

        city = ' '.join(args)
        await weather_command(context, city)


    # Used for testing various stuff before implementing them on actual command.
    @bot.command(name='test')
    async def test(context):
        await remove_command_message(context.message)
