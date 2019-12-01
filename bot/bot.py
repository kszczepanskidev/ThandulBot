import discord
from discord.ext import commands

from .environment import bot_environment
from bot.handlers.handlers import init_handlers

bot = commands.Bot(command_prefix=bot_environment.command_symbol)
init_handlers(bot)