from discord import Object

from .system_events import *
from .reactions import handle_reaction_event

def bindEvents(bot, commands_tree):

    # Connected to Discord.
    @bot.event
    async def on_ready():
        await commands_tree.sync()
        handle_on_ready(bot)

    # Message error.
    @bot.event
    async def on_error(event, *args, **kwargs):
        handle_on_error(event, args, kwargs)

    # Message reaction added.
    @bot.event
    async def on_raw_reaction_add(event):
        await handle_reaction_event(bot, event)

    # Message reaction removed.
    @bot.event
    async def on_raw_reaction_remove(event):
        await handle_reaction_event(bot, event)
