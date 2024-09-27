from discord import Client, Intents, app_commands
from .logger import start_logger
import locale

from .environment import bot_environment
from bot.handlers.handlers import init_handlers

locale.setlocale(locale.LC_ALL, bot_environment.locale)
start_logger()
bot = Client(intents=Intents.all())
commands_tree = app_commands.CommandTree(bot)
init_handlers(bot, commands_tree)
