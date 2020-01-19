from .events import bindEvents
from .commands import bindCommands

def init_handlers(bot):
    bindEvents(bot)
    bindCommands(bot)