import os
from dotenv import load_dotenv
from collections import namedtuple

load_dotenv()
Environment = namedtuple(
    'Environment',
    ['token', 'guild', 'channels', 'command_symbol', 'mention_role_id', 'admin_id' ]
)

bot_environment = Environment(
    os.getenv('DISCORD_TOKEN'),
    os.getenv('DISCORD_GUILD'),
    str(os.getenv('DISCORD_RPG_CHANNELS')).split(';'),
    '!',
    os.getenv('DISCORD_DND_ROLE_ID'),
    os.getenv('DISCORD_ADMIN_ID'),
)