import discord
from discord.ext import commands
from .logger import start_logger
import locale

from .environment import bot_environment
from bot.handlers.handlers import init_handlers

locale.setlocale(locale.LC_ALL, bot_environment.locale)
start_logger()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=bot_environment.command_symbol, intents=intents)
init_handlers(bot)
