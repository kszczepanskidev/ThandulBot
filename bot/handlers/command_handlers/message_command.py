from ..helpers import handle_user_error

async def send_message_command(interaction, channel, message):
    try:
        channel = interaction.client.get_channel(int(channel))
    except:
        await handle_user_error(interaction, f"send_message_command: Channel id can't be parsed. {channel}")
        return

    if not channel:
        await handle_user_error(interaction, f"send_message_command: Channel with given id don't exist. {channel}")
        return

    await channel.send(" ".join(message))
