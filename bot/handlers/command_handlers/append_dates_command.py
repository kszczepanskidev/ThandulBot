from re import findall
from datetime import datetime, timedelta

from ...environment import emotes
from ..helpers import handle_user_error

# Edits Embed in given message by appending new dates.
async def append_dates_command(interaction, message, dates):
    date_emotes = [emote for emote in emotes if str(emote) != u'\u274c']

    # Fetch message to edit.
    message_to_edit = await interaction.channel.fetch_message(int(message))

    # Extract dates from command parameter.
    if '-' in dates:
        # Extract range of dates from command parameter.
        dates_range = [datetime.strptime(date, '%d.%m').replace(year=datetime.now().year) for date in dates.split('-', 1)]
        dates = [dates_range[0] + timedelta(days=shift) for shift in range((dates_range[1] - dates_range[0]).days + 1)]
        dates = [str(date.strftime('%d.%m;')) for date in dates]
    else:
        # Extract singular dates from command parameter.
        dates = findall(r'(\d{1,2}\.\d{1,2};{1})', dates + ';')

    current_dates_count = len(message_to_edit.reactions) - 1

    # Check if there are any dates and if their amount isn't to big.
    if len(dates) == 0:
        await handle_user_error(interaction, 'add_dates_command', f'No dates found in {dates}')
        return
    elif len(dates) + current_dates_count > len(emotes):
        await handle_user_error(interaction, 'add_dates_command', f'Too many dates found in {dates}')
        return

    new_dates = '\n\n'.join(['{}{}{}'.format(emotes[it + current_dates_count], u'\u00A0'*4, str(datetime.strptime(date, '%d.%m;').replace(year=datetime.now().year).strftime('%d.%m, %A'))) for (it, date) in enumerate(dates)])

    new_embed = message_to_edit.embeds[0]
    new_embed.description += '\n\n'
    new_embed.description += new_dates

    await message_to_edit.edit(embed=new_embed)

    for emote in date_emotes[current_dates_count:current_dates_count + len(dates)]:
        await message_to_edit.add_reaction(emote)
