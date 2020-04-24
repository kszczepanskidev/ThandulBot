from ..environment import bot_environment
from .helpers import remove_command_message, should_perform_command
from .check_dates_command import check_dates_command
from .add_dates_command import add_dates_command
from .weather_command import weather_command
from .animals_commands import postAnimal, postRandomAnimal,  postAnimalPhoto

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

    @bot.command(name='cat')
    async def cat(context, *args):
        await postAnimal(context, 'cat')

    @bot.command(name='dog')
    async def dog(context, *args):
        await postAnimal(context, 'dog')

    @bot.command(name='fox')
    async def fox(context, *args):
        await postAnimal(context, 'fox')

    @bot.command(name='duck')
    async def fox(context, *args):
        await postAnimal(context, 'duck')

    @bot.command(name='goat')
    async def fox(context, *args):
        await postAnimal(context, 'goat')

    @bot.command(name='animal')
    async def fox(context, *args):
        await postRandomAnimal(context)

    # Used for testing various stuff before implementing them on actual command.
    @bot.command(name='test')
    async def test(context):
        await remove_command_message(context.message)
