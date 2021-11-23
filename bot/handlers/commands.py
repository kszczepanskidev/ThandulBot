from discord.ext import commands

from ..environment import bot_environment
from .command_categories.admin_category import AdminCommands
from .command_categories.rpg_category import RPGCommands
from .command_categories.information_category import Information
from .command_categories.animal_photo_category import AnimalRandomPhotos


# Register commands categories.
def bindCommands(bot):
    bot.add_cog(AdminCommands())
    bot.add_cog(RPGCommands())
    bot.add_cog(Information())
    bot.add_cog(AnimalRandomPhotos())