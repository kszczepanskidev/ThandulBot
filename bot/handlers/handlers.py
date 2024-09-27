from asyncio import run

from .events import bindEvents
from .commands import bindCommands

def init_handlers(bot, commands_tree):
    bindEvents(bot, commands_tree)
    bindCommands(commands_tree)
