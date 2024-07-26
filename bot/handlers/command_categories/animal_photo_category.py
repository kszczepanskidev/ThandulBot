from discord import app_commands, Interaction
from discord.ext import commands
from typing import Literal

from ..command_handlers.animals_commands import post_animal_command, post_random_animal_command

class AnimalRandomPhotos(app_commands.Group):
    """
    Commands that post random photos of animals.
    """

    @app_commands.command(name='photo')
    @app_commands.describe(animal='animal type to get random photo of.')
    async def cat(self, interaction: Interaction, animal: Literal['cat', 'dog', 'fox', 'duck']):
        """
        Posts random photo of a selected animal.

        Parameters:
            - animal: animal type to get random photo of.
        """
        await post_animal_command(interaction, animal)

    @app_commands.command(name='animal')
    async def animal(self, interaction: Interaction):
        """
        Posts random photo of an random animal.
        """
        await post_random_animal_command(interaction)
