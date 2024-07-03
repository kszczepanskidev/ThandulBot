import logging
from datetime import datetime, timedelta
from threading import Timer
from asyncio import run_coroutine_threadsafe, get_running_loop
from bot import bot

from ..environment import bot_environment, emotes

_active_timer = None
_running_loop = None

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
    lines = [line.replace('***', '').replace('**', '') for line in description.split('\n') if line != '']

    # Extract GM id from message and get his players from config.
    gm_id = message.content.split('GM:')[-1][3:-1]
    gm_players_ids = bot_environment.gm_list[int(gm_id)]

    # Extract reactions and users from message.
    reactions = message.reactions

    hasHighlightedLine = False
    # Update all lines to avoid async errors.
    for (it, line) in enumerate(lines):
        # Get usernames for edited reaction.
        emoji = line[0]
        reaction = [reaction for reaction in reactions if str(reaction) == str(emoji)][0]
        users = [user async for user in reaction.users()]
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

        # Make text bold when all users voted or someone voted on ❌ and bold italic if one vote is missing.
        missing_votes_counter = [id in [user.id for user in voting_users] for id in gm_players_ids].count(False)
        if missing_votes_counter < 2 or str(reaction) == u'\u274c':
            hasHighlightedLine = True
            markdown_modifier = '*' * (3 if missing_votes_counter == 1 else 2)
            line = markdown_modifier + line + markdown_modifier

        lines[it] = line

    cant_users = [user.name async for user in [reaction for reaction in message.reactions if str(reaction) == u'\u274c'][0].users() if user.id != bot.user.id]
    if len(cant_users) > 0 and len([line for line in lines if u'\u274c' in str(line)]) == 0:
        hasHighlightedLine = True
        lines.append('**' + u'\u274c' + u'\u00A0'*4 + f"Blibors [{', '.join(cant_users)}]**")

    # Update message with edited embed.
    embed.description = '\n\n'.join(lines)
    await message.edit(embed=embed)

    gm_user = bot.get_user(int(gm_id))
    player_users = [bot.get_user(int(player_id)) for player_id in gm_players_ids]
    if hasHighlightedLine and gm_user is not None:
        logging.info(f'Notifying {gm_user} and {player_users}')
        # await setupDelayedNotifyMessage([gm_user] + player_users, embed)

async def setupDelayedNotifyMessage(users, embed):
    global _active_timer, _running_loop

    # Invalidate previous timer.
    if _active_timer != None:
        _active_timer.cancel()

    # Setup timer to send notify message after 1 minute.
    _running_loop = get_running_loop()
    _active_timer = Timer(60, callAsyncNotifyFunction, args=[users, embed])
    _active_timer.start()

def callAsyncNotifyFunction(users, embed):
    global _running_loop

    # Safely run async function with `asyncio.run_coroutine_threadsafe`.
    run_coroutine_threadsafe(notifyAboutFullVoteDate(users, embed), _running_loop)

async def notifyAboutFullVoteDate(users, embed):
    for user in users:
        try:
            await user.send('Votes changed!', embed=embed)
        except Exception as e:
            logging.error(f'failed to sent message to {user} - {e}')
