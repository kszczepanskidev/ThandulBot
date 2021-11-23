from re import findall
import logging
from datetime import datetime

from ...environment import bot_environment, emotes
from ..helpers import get_role_mention

# Edits Embed in given message by appending new dates.
async def append_dates_command(context, message, dates):

    # Fetch message to edit.
    message_to_edit = await context.fetch_message(int(message))

    # Extract dates from command parameter.
    dates = findall(r'(\d{1,2}\.\d{1,2};{1})', dates + ';')

    current_dates_count = len(message_to_edit.reactions) - 1

    # Check if there are any dates and if their amount isn't to big.
    if len(dates) == 0:
        logging.error('add_dates_command: No dates found')
        return
    elif len(dates) + current_dates_count > len(emotes):
        logging.error('add_dates_command: Too many dates found')
        return

    new_dates = '\n\n'.join(['{}{}{}'.format(emotes[it + current_dates_count], u'\u00A0'*4, str(datetime.strptime(date, '%d.%m;').replace(year=datetime.now().year).strftime('%d.%m, %A'))) for (it, date) in enumerate(dates)])

    new_embed = message_to_edit.embeds[0]
    new_embed.description += '\n\n'
    new_embed.description += new_dates

    await message_to_edit.edit(embed=new_embed)

    for i in range(current_dates_count, current_dates_count + len(dates)):
        await message_to_edit.add_reaction(emotes[i])