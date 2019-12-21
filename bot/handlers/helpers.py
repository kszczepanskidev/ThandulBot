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
    return check_author_permission(context.author.id) and check_channel_name(context.guild.id, context.channel.name)

# Checks if user that issued command is in permissions list.
def check_author_permission(author_id):
    return str(author_id) == str(bot_environment.admin_id)

# Checks if user issued command in channel from config file.
def check_channel_name(guild_id, channel_name):
    return str(channel_name) in bot_environment.channels[guild_id]

# Get role mention that is present on server that command was issued at.
def get_role_mention(context):
    try:
        mentionable_role = bot_environment.mention_role_ids[context.guild.id][context.channel.name]
        if mentionable_role in [role.id for role in context.guild.roles]:
            return mentionable_role
    except:
        logging.error('No role to mention.')
        raise Exception()