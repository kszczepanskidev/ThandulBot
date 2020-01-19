from .system_events import *

def bindEvents(bot):

    # Connected to Discord.
    @bot.event
    async def on_ready():
        handle_on_ready(bot)

    # Message error.
    @bot.event
    async def on_error(event, *args, **kwargs):
        handle_on_error(event, args, kwargs)