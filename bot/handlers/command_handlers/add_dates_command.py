from re import findall
from discord import Embed
import logging
from datetime import datetime, timedelta

from ...environment import bot_environment, emotes
from ..helpers import get_role_mention

# Sends message with rich embed with dates given in command message
# assigning emote to each and reactions for voting under sent message.
async def add_dates_command(context, dates, customMessage):

    if ';' in dates:
        # Extract singular dates from command parameter.
        dates = findall(r'(\d{1,2}\.\d{1,2};{1})', dates + ';')
    elif '-' in dates:
        # Extract range of dates from command parameter.
        dates_range = [datetime.strptime(date, '%d.%m').replace(year=datetime.now().year) for date in dates.split('-', 1)]
        dates = [dates_range[0] + timedelta(days=shift) for shift in range((dates_range[1] - dates_range[0]).days + 1)]
        dates = [str(date.strftime('%d.%m;')) for date in dates]
    else:
        dates = []

    # Check if there are any dates and if their amount isn't to big.
    if len(dates) == 0:
        logging.error('add_dates_command: No dates found')
        return
    elif len(dates) > len(emotes):
        logging.error('add_dates_command: Too many dates found')
        return

    # Create Rich Embed with given dates.
    embed = Embed(
        title='Terminy na kolejny tydzień. Oznaczcie które dni wam pasują:' if (customMessage == None or customMessage == '') else customMessage,
        type='rich',
        description= '\n\n'.join(['{}{}{}'.format(emotes[it], u'\u00A0'*4, str(datetime.strptime(date, '%d.%m;').replace(year=datetime.now().year).strftime('%d.%m, %A'))) for (it, date) in enumerate(dates)]),
    )

    # Get players to mention
    players = bot_environment.gm_list[context.author.id]
    player_mentions = [f'<@{id}>' for id in players]
    if len(player_mentions) == 0: return

    # Send message with proper mention and rich embed.
    dates_msg = await context.send(f'Gracze: {" ".join(player_mentions)}\nGM: <@{context.author.id}>', embed=embed)

    # Add reactions for voting.
    for i in range(0, len(dates)):
        await dates_msg.add_reaction(emotes[i])

    # Add `X` reaction for signaling no date chosen.
    await dates_msg.add_reaction('❌')