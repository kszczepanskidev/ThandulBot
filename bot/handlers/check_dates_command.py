from re import search
import logging

from ..environment import bot_environment
from .helpers import get_role_mention

# Checks last message with dates for reactions.
# Extracts unique users that selected any date.
# Sends mention for user that didn't reacted yet.
# Sends summary if everyone voted, with selected or none dated.
async def check_dates_command(ctx):

    # Check if config file have role mention for current server.
    try:
        role_mention_id = get_role_mention(ctx)
    except:
        return

    # Get last message with dates based on containing rich embed.
    messages = await ctx.message.channel.history(limit=200).flatten()
    bot_messages = [msg for msg in messages if str(msg.author.id) == bot_environment.bot_id]
    last_dates_message = next(msg for msg in bot_messages if len([embed for embed in msg.embeds if embed.type == 'rich']) > 0)

    # Get ids of mentinable users for given server from config file and cross-check it with ids of all users on the server.
    # Exits if there is no matching users or config file doesn't include id of current server.
    guild_member_ids = [member.id for member in ctx.guild.members]
    try:
        mentionable_members = [member_id for member_id in bot_environment.user_ids[ctx.guild.id] if member_id in guild_member_ids]
        if len(mentionable_members) == 0:
            logging.error('No mentionable users.')
            return
    except:
        logging.error('No server id in config file.')
        return

    # Get ids of users that gave any reaction under last dates message.
    last_dates_message_reactions = [await reaction.users().flatten() for reaction in last_dates_message.reactions]
    users_that_reacted = set([str(user.id) for users in last_dates_message_reactions for user in users if str(user.id) != bot_environment.bot_id])

    # Check if there are users that didn't reacted to mention them in a message asking to vote.
    users_to_mention = [user for user in mentionable_members if str(user) not in users_that_reacted]
    if len(users_to_mention) > 0:
        await ctx.send(' '.join(['<@{}>'.format(user_id) for user_id in users_to_mention]) + ' proszę o określenie się co do zaproponowanych terminów.')
        return

    # If all given in bot setup users voted, check for selected dates by them.
    reactions_with_full_votes = [reaction.emoji for reaction in last_dates_message.reactions if [user.id for user in await reaction.users().flatten() if str(user.id) != bot_environment.bot_id] == mentionable_members]
    dates_selected_by_all = [search(r'(\d{1,2}\.\d{1,2})', date).group(1) for date in last_dates_message.embeds[0].description.split('\n\n') for reaction in reactions_with_full_votes if reaction in date]

    # Sends message with selected dates or information that no date was selected by everyone.
    message = '<@&{}> Wszyscy zagłosowali, '.format(role_mention_id)
    if len(dates_selected_by_all) > 0:
        message += 'pasujące terminy: {}'.format(', '.join(dates_selected_by_all))
    else:
        message += 'brak pasujących terminów :('
    await ctx.send(message)