from ...environment import bot_environment
from ..helpers import handle_user_error

from os import system

# Restarts Foundry VTT instance for invoking GM.
async def restart_foundry_command(interaction, instance):
    user_id = interaction.user.id
    instances = [instance.capitalize() for instance in bot_environment.foundry_admins[user_id]]

    instance = instance.capitalize()
    instance_to_restart = instance if instance is not None and instance in instances else instances[0]

    system(f'pm2 reload FoundryVTT{instance_to_restart}')
    await interaction.response.send_message(content=f'Restarting FoundryVTT{instance_to_restart} instance.')
