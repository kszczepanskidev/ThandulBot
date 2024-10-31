import logging
from datetime import datetime, timedelta
from threading import Timer
from asyncio import run_coroutine_threadsafe, get_running_loop

from ..environment import bot_environment, emotes
from ..database import DatesNotifyDatabase, dates_notify_database

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

    __has_one_to_go = False
    __has_all_players = False
    __has_cant_players = False
    # Update all lines to avoid async errors.
    for (it, line) in enumerate(lines):
        # Get usernames for edited reaction.
        emoji = line[0]
        reaction = [reaction for reaction in reactions if str(reaction) == str(emoji)][0]
        users = [user async for user in reaction.users()]
        voting_users = [user for user in users if user.id != bot.user.id]
        usernames = [user.name for user in voting_users]

        # Remove line for ❌ reaction if no one voted.
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
        match missing_votes_counter:
            case 0:
                __has_all_players = True
            case 1:
                __has_one_to_go = True
        if missing_votes_counter < 2 or str(reaction) == u'\u274c':
            markdown_modifier = '*' * (3 if __has_one_to_go else 2)
            line = markdown_modifier + line + markdown_modifier

        lines[it] = line

    cant_users = [user.name async for user in [reaction for reaction in message.reactions if str(reaction) == u'\u274c'][0].users() if user.id != bot.user.id]
    hasCantUsers = len(cant_users) > 0
    if hasCantUsers:
        __has_cant_players = True
    if hasCantUsers and len([line for line in lines if u'\u274c' in str(line)]) == 0:
        lines.append('**' + u'\u274c' + u'\u00A0'*4 + f"Blibors [{', '.join(cant_users)}]**")

    # Update message with edited embed.
    embed.description = '\n\n'.join(lines)
    await message.edit(embed=embed)

    gm_user = bot.get_user(int(gm_id))
    player_users = [bot.get_user(int(player_id)) for player_id in gm_players_ids]
    notify_flags = [__has_one_to_go, __has_all_players, __has_cant_players]
    if (True in notify_flags) and gm_user is not None:
        await setupDelayedNotifyMessage(event, [gm_user] + player_users, embed, channel, __has_one_to_go, __has_all_players, __has_cant_players)

async def setupDelayedNotifyMessage(event, users, embed, channel, has_one_to_go, has_all_players, has_cant_players):
    global _active_timer, _running_loop

    # Invalidate previous timer.
    if _active_timer != None:
        _active_timer.cancel()

    # Setup timer to send notify message after 1 minute.
    _running_loop = get_running_loop()
    _active_timer = Timer(6, callAsyncNotifyFunction, args=[event, users, embed, channel, has_one_to_go, has_all_players, has_cant_players])
    _active_timer.start()

def callAsyncNotifyFunction(event, users, embed, channel, has_one_to_go, has_all_players, has_cant_players):
    global _running_loop

    # Safely run async function with `asyncio.run_coroutine_threadsafe`.
    run_coroutine_threadsafe(notifyAboutFullVoteDate(event, users, embed, channel, has_one_to_go, has_all_players, has_cant_players), _running_loop)

async def notifyAboutFullVoteDate(event, users, embed, channel, has_one_to_go, has_all_players, has_cant_players):
    db_log = dates_notify_database.get_log(event.message_id)
    if db_log is None:
        dates_notify_database.add_log(dates_notify_database.DatesNotifyLog(event.message_id, has_one_to_go, has_all_players, has_cant_players))
        db_log = dates_notify_database.DatesNotifyLog(event.message_id)
    else:
        dates_notify_database.update_log(dates_notify_database.DatesNotifyLog(db_log.message_id, db_log.had_one_to_go or has_one_to_go, db_log.had_all_players or has_all_players, db_log.had_cant_players or has_cant_players))

    sendDM = False
    sendChannelMessage = False

    # Send channel message if it's first time when any option has n-1 votes.
    if not db_log.had_one_to_go and has_one_to_go:
        sendChannelMessage = True

    # Send DM when any option has all votes for the first time or after there was can't vote and it got removed.
    if ((not db_log.had_all_players) or db_log.had_cant_players) and has_all_players and not has_cant_players:
        sendDM = True

    # Send DM when there's can't vote for the first time or after there was option with all votes.
    if (db_log.had_all_players or not db_log.had_cant_players) and has_cant_players:
        sendDM = True

    if sendDM:
        logging.info(f'Notifying {users}')
        for user in users:
            try:
                await user.send('Votes changed!', embed=embed)
            except Exception as e:
                logging.error(f'Failed to send message to {user} - {e}')
    elif sendChannelMessage:
        logging.info(f'Notifying channel {channel}')
        try:
            role_mention = int(bot_environment.role_mentions[int(event.guild_id)][int(event.channel_id)])
            await channel.send(f'<@&{role_mention}> One more vote and we have it')
        except Exception as e:
            logging.error(f'Failed to send message to {channel}')
