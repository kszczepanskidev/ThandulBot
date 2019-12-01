import os
from dotenv import load_dotenv
from collections import namedtuple

load_dotenv()
Environment = namedtuple(
    'Environment',
    ['token', 'guild', 'channels', 'command_symbol' ]
)

bot_environment = Environment(
    os.getenv('DISCORD_TOKEN'),
    os.getenv('DISCORD_GUILD'),
    str(os.getenv('DISCORD_RPG_CHANNELS')).split(';'),
    '!',
)