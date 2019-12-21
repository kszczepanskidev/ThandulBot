from ..environment import bot_environment
from .helpers import remove_command_message, should_perform_command
from .check_dates_command import check_dates_command
from .add_dates_command import add_dates_command

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


    # Used for testing various stuff before implementing them on actual command.
    @bot.command(name='test')
    async def test(context):
        await remove_command_message(context.message)
        try:
            print(bot_environment.user_ids[context.guild.id])
        except:
            print('Command executed but no user ids for current server')
            return
