from discord.ext import commands

from ..environment import bot_environment
from .command_categories.admin_category import AdminCommands
from .command_categories.rpg_category import RPGCommands
from .command_categories.information_category import Information
from .command_categories.animal_photo_category import AnimalRandomPhotos


# Register commands categories.
async def bindCommands(bot):
    await bot.add_cog(AdminCommands())
    await bot.add_cog(RPGCommands())
    await bot.add_cog(Information())
    await bot.add_cog(AnimalRandomPhotos())
