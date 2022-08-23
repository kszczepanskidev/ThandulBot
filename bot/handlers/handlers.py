from asyncio import run

from .events import bindEvents
from .commands import bindCommands

def init_handlers(bot):
    bindEvents(bot)
    run(bindCommands(bot))
