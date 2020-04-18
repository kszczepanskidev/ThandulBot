import logging

from ..environment import bot_environment

# Removes message with command if have permissions.
async def remove_command_message(message):
    try:
        await message.delete()
    except:
        logging.error('Failed to delete message.')
        return

def should_perform_command(context):
    return check_author_permission(context.command.name, context.channel.id, context.author.id) and check_channel_id(context.command.name, context.channel.id)

# Checks if user that issued admin command is in permissions list.
def check_author_permission(command, channel_id, author_id):
    if command in bot_environment.admin_commands:
        return str(author_id) == str(bot_environment.admin_id)
    else:
        return True

# Checks if user issued command in correct channel from config file.
def check_channel_id(command, channel_id):
    return channel_id in bot_environment.command_channels[command]

# Get role mention that is present on server that command was issued at.
def get_role_mention(context):
    try:
        mentionable_role = bot_environment.mention_role_ids[context.guild.id][context.channel.name]
        if mentionable_role in [role.id for role in context.guild.roles]:
            return mentionable_role
    except:
        logging.error('No role to mention.')
        raise Exception()
