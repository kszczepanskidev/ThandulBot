from re import findall
from discord import Embed
from datetime import datetime, timedelta

from ...environment import bot_environment, emotes
from ..helpers import handle_user_error

# Sends message with rich embed with dates given in command message
# assigning emote to each and reactions for voting under sent message.
async def add_dates_command(interaction, dates, customMessage):
    date_emotes = [emote for emote in emotes if str(emote) != u'\u274c']

    if '-' in dates:
        # Extract range of dates from command parameter.
        dates_range = [datetime.strptime(date, '%d.%m').replace(year=datetime.now().year) for date in dates.split('-', 1)]
        dates = [dates_range[0] + timedelta(days=shift) for shift in range((dates_range[1] - dates_range[0]).days + 1)]
        dates = [str(date.strftime('%d.%m;')) for date in dates]
    else:
        # Extract singular dates from command parameter.
        dates = findall(r'(\d{1,2}\.\d{1,2};{1})', dates + ';')

    dates = [date.replace(';', f'.{datetime.now().year};') for date in dates]

    # Check if there are any dates and if their amount isn't to big.
    if len(dates) == 0:
        await handle_user_error(interaction, 'add_dates_command', f'No dates found in {dates}')
        return
    elif len(dates) > len(date_emotes):
        await handle_user_error(interaction, 'add_dates_command', f'Too many dates found in {dates}')
        return

    # Create Rich Embed with given dates.
    embed = Embed(
        title='Terminy na kolejny tydzień. Oznaczcie które dni wam pasują:' if customMessage == None else customMessage,
        type='rich',
        description= '\n\n'.join(['{}{}{}'.format(date_emotes[it], u'\u00A0'*4, str(datetime.strptime(date, '%d.%m.%Y;').replace(year=datetime.now().year).strftime('%d.%m, %A'))) for (it, date) in enumerate(dates)]),
    )

    # Get players to mention
    players = bot_environment.gm_list[interaction.user.id]
    player_mentions = [f'<@{id}>' for id in players]
    if len(player_mentions) == 0: return

    # Send message with proper mention and rich embed.
    await interaction.response.send_message(f'Gracze: {" ".join(player_mentions)}\nGM: <@{interaction.user.id}>', embed=embed)

    # Fetch created message.
    dates_msg = await interaction.original_response()

    # Add reactions for voting.
    msg_emotes = date_emotes[:len(dates)]
    msg_emotes.append(u'\u274c')
    for emote in msg_emotes:
        await dates_msg.add_reaction(emote)
