from ..environment import bot_environment
from .helpers import remove_command_message, check_author_permission
from .check_dates_command import check_dates_command
from .add_dates_command import add_dates_command

def bindCommands(bot):

    @bot.command(name='addDates')
    async def add_dates(ctx, dates):
        await remove_command_message(ctx.message)
        if not check_author_permission(ctx.author.id):
            return

        await add_dates_command(ctx, dates)

    @bot.command(name='twat')
    async def check_dates(ctx):
        await remove_command_message(ctx.message)
        if not check_author_permission(ctx.author.id):
            return

        await check_dates_command(ctx)


    # Used for testing various stuff before implementing them on actual command.
    @bot.command(name='test')
    async def test(ctx):
        await remove_command_message(ctx.message)
        try:
            print(bot_environment.user_ids[ctx.guild.id])
        except:
            print('Command executed but no user ids for current server')
            return
