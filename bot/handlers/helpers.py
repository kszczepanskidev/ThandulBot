import logging

from ..environment import bot_environment

# Logs error message and send ephemeral response with error description.
async def handle_user_error(interaction, function, message):
    logging.error(f'{function}:{message}')
    await interaction.response.send_message(message, ephemeral=True)

# Checks if command can be called by given user in given channel.
def should_perform_command(interaction):
    if not check_author_permission(interaction.command.name, interaction.user.id):
        handle_user_error(interaction, 'should_perform_command', f'user without permissions to use command. {interaction.user.name} {interaction.message.content}')
        return False

    if not check_channel_id(interaction.command.name, interaction.channel.id):
        handle_user_error(interaction, 'should_perform_command', f'command called in wrong channel. {interaction.channel.name} {interaction.message.content}')
        return False

    return True

# Checks if command can be called by given game master in given channel.
def should_perform_gm_command(interaction):
    gm_list = [str(gm_id) for gm_id in bot_environment.gm_list.keys()]
    if not str(interaction.user.id) in gm_list:
        handle_user_error(interaction, 'should_perform_gm_command', f'user not defined in game masters list. {interaction.user.name} {interaction.message.content}')
        return False

    if not check_channel_id(interaction.command.name, interaction.channel.id):
        handle_user_error(interaction, 'should_perform_gm_command', f'command called in wrong channel. {interaction.channel.name} {interaction.message.content}')
        return False

    return True

# Checks if user that issued admin command is in permissions list.
def check_author_permission(command, author_id):
    if command in bot_environment.admin_commands:
        return str(author_id) == str(bot_environment.admin_id)
    else:
        return True

# Checks if user issued command in correct channel from config file.
def check_channel_id(command, channel_id):
    if command in bot_environment.command_channels.keys():
        return channel_id in bot_environment.command_channels[command]
    else:
        return True
