from discord.ext import commands
from ..command_handlers.animals_commands import post_animal_command, post_random_animal_command

class AnimalRandomPhotos(commands.Cog):
    """
    Commands that postrandom photos of animals.
    """

    @commands.command(name='cat')
    async def cat(self, context):
        """
        Posts random photo of a cat.
        """
        await post_animal_command(context, 'cat')

    @commands.command(name='dog')
    async def dog(self, context):
        """
        Posts random photo of a dog.
        """
        await post_animal_command(context, 'dog')

    @commands.command(name='fox')
    async def fox(self, context):
        """
        Posts random photo of a fox.
        """
        await post_animal_command(context, 'fox')

    @commands.command(name='duck')
    async def fox(self, context):
        """
        Posts random photo of a duck..
        """
        await post_animal_command(context, 'duck')

    @commands.command(name='goat')
    async def fox(self, context):
        """
        Posts random photo of a goat.
        """
        await post_animal_command(context, 'goat')

    @commands.command(name='animal')
    async def fox(self, context):
        """
        Posts random photo of an random animal.
        """
        await post_random_animal_command(context)