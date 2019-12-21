from re import findall
from discord import Embed, Emoji, utils
from itertools import zip_longest
from math import floor
import logging

from ..environment import bot_environment, emotes
from .helpers import get_role_mention

# Sends message with rich embed with dates given in command message
# assigning emote to each and reactions for voting under sent message.
async def add_dates_command(context, dates):

    # Extract dates from command parameter.
    dates = findall(r'(\d{1,2}\.\d{1,2};{1})', dates + ';')

    # Check if there are any dates and if their amount isn't to big.
    if len(dates) == 0:
        logging.error('add_dates_command: No dates found')
        return
    elif len(dates) > len(emotes):
        logging.error('add_dates_command: Too many dates found')
        return

    if len(dates) > 5:
        middle_point = floor(len(dates) / 2) + 1
        split_dates = zip_longest(dates[:middle_point], dates[middle_point:])

    # Create Rich Embed with given dates.
    embed = Embed(
        title='Terminy na kolejny tydzień. Oznaczcie które dni wam pasują:',
        type='rich',
        description= '\n\n'.join([('{}{}{}' if date2 is None else '{}{}{}{}{}{}{}').format(emotes[it], u'\u00A0'*4, str(date1)[:-1], u'\u00A0'*12, emotes[it + middle_point], u'\u00A0'*4, str(date2)[:-1]) for (it, (date1, date2)) in enumerate(split_dates)]),
    )

    # Check if config file have role mention for current server.
    try:
        role_mention_id = get_role_mention(context)
    except:
        return

    # Send message with proper mention and rich embed.
    dates_msg = await context.send('<@&{}>'.format(role_mention_id), embed=embed)

    # Add reactions for voting.
    for i in range(0, len(dates)):
        await dates_msg.add_reaction(emotes[i])