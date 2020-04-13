import logging

from ..environment import bot_environment, emotes

async def handle_reaction_event(bot, event):
    # Do not handle reactions made by bot.
    if event.user_id == bot.user.id:
        logging.info('handle_reaction_event: Reaction from bot')
        return

    channel = await bot.fetch_channel(event.channel_id)
    message = await channel.fetch_message(event.message_id)

    # Do not handle reactions for messages without embed or from other user than bot.
    if len(message.embeds) == 0:
        logging.info('handle_reaction_event: Message without embeds')
        return
    if message.author.id != bot.user.id:
        logging.info('handle_reaction_event: Not a message from bot')
        return

    # Get text with dates split into lines.
    embed = message.embeds[0]
    description = embed.description
    lines = [line for line in description.split('\n') if line != '']

    # Update all lines to avoid async errors.
    for (it, line) in enumerate(lines):
        # Get usernames for edited reaction.
        emoji = line[0]
        reactions =  message.reactions
        reaction = [reaction for reaction in reactions if str(reaction) == str(emoji)][0]
        users = await reaction.users().flatten()
        usernames = [user.name for user in users if user.id != bot.user.id]

        # Edit line with edited reaction.
        line = line.split('[')[0]
        if len(usernames) > 0:
            if line[-1] != ' ':
                line += ' '
            line += f"[{', '.join(usernames)}]"
        lines[it] = line

    # Update message with edited embed.
    embed.description = '\n\n'.join(lines)
    await message.edit(embed=embed)