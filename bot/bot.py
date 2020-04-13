import discord
from discord.ext import commands
from .logger import start_logger
import locale

from .environment import bot_environment
from bot.handlers.handlers import init_handlers

locale.setlocale(locale.LC_ALL, bot_environment.locale)
start_logger()
bot = commands.Bot(command_prefix=bot_environment.command_symbol)
init_handlers(bot)