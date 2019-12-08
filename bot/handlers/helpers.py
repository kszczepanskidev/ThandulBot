import logging

from ..environment import bot_environment

# Removes message with command if have permissions.
async def remove_command_message(message):
    try:
        await message.delete()
    except:
        logging.error('Failed to delete message.')
        return

# Checks if user that issued command is in permissions list.
def check_author_permission(author_id):
    return str(author_id) == str(bot_environment.admin_id)

# Get role mention that is present on server that command was issued at.
def get_role_mention(ctx):
    try:
        mentionable_role = bot_environment.mention_role_ids[ctx.guild.id]
        if mentionable_role in [role.id for role in ctx.guild.roles]:
            return mentionable_role
    except:
        logging.error('No role to mention.')
        raise Exception()