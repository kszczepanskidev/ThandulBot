import logging
from datetime import datetime, timedelta
from bot import bot

from ..environment import bot_environment, emotes

bot.last_message_sent_at = datetime(2000, 1, 1)

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

    if event.emoji.name not in emotes:
        logging.info(f'handle_reaction_event: Not supported emoji - {event.emoji.name}')
        return

    # Get text with dates split into lines.
    embed = message.embeds[0]
    description = embed.description
    lines = [line.replace('**', '') for line in description.split('\n') if line != '']

    # Extract GM id from message and get his players from config.
    gm_id = message.content.split('GM:')[-1][3:-1]
    gm_players_ids = bot_environment.gm_list[int(gm_id)]

    hasDateWithAllVotes = False
    # Update all lines to avoid async errors.
    for (it, line) in enumerate(lines):
        # Get usernames for edited reaction.
        emoji = line[0]
        reactions =  message.reactions
        reaction = [reaction for reaction in reactions if str(reaction) == str(emoji)][0]
        users = await reaction.users().flatten()
        voting_users = [user for user in users if user.id != bot.user.id]
        usernames = [user.name for user in voting_users]

        # Remove line for ❌ reaction if noone voted.
        if str(reaction) == u'\u274c' and len(voting_users) == 0:
            lines.pop(it)
            continue

        # Edit line with edited reaction.
        line = line.split('[')[0]
        if len(usernames) > 0:
            if line[-1] != ' ':
                line += ' '
            line += f"[{', '.join(usernames)}]"

        # Make text bold when all users voted or someone voted on ❌.
        if all(id in [user.id for user in voting_users] for id in gm_players_ids) or str(reaction) == u'\u274c':
            hasDateWithAllVotes = True
            line = '**' + line + '**'

        lines[it] = line

    cant_users = [user.name for user in await [reaction for reaction in message.reactions if str(reaction) == u'\u274c'][0].users().flatten() if user.id != bot.user.id]
    if len(cant_users) > 0 and len([line for line in lines if u'\u274c' in str(line)]) == 0:
        lines.append('**' + u'\u274c' + u'\u00A0'*4 + f"Blibors [{', '.join(cant_users)}]**")

    # Update message with edited embed.
    embed.description = '\n\n'.join(lines)
    await message.edit(embed=embed)

    gm_user = bot.get_user(int(gm_id))
    if hasDateWithAllVotes and gm_user is not None:
        await notifyAboutFullVoteDate(gm_user, embed)

async def notifyAboutFullVoteDate(gm_user, embed):
    current_date = datetime.now()
    if bot.last_message_sent_at + timedelta(minutes=2) <= current_date:
        bot.last_message_sent_at = current_date
        await gm_user.send('Votes changed!', embed=embed)
