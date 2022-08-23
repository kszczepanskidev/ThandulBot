import logging

async def send_message_command(context, args):

    if not len(args) >= 2:
        logging.error(f'send_message_command: Not enough arguments passed. {args}')
        return

    try:
        channel = context.bot.get_channel(int(args[0]))
    except:
        logging.error(f"send_message_command: Channel id can't be parsed. {args[0]}")
        return

    if not channel:
        logging.error(f"send_message_command: Channel with given id don't exist. {args[0]}")
        return

    await channel.send(" ".join(args[1:]))
